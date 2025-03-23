import asyncio
import json
import logging
import marshal
from hashlib import md5
from pathlib import Path
from time import perf_counter, time_ns
from typing import Callable, Iterable, Optional, Tuple

import polars as pl
import pytest
from starkware.cairo.common.dict import DictManager
from starkware.cairo.lang.builtins.all_builtins import ALL_BUILTINS
from starkware.cairo.lang.cairo_constants import DEFAULT_PRIME
from starkware.cairo.lang.compiler.ast.cairo_types import (
    CairoType,
    TypeStruct,
    TypeTuple,
)
from starkware.cairo.lang.compiler.cairo_compile import compile_cairo, get_module_reader
from starkware.cairo.lang.compiler.identifier_definition import (
    StructDefinition,
    TypeDefinition,
)
from starkware.cairo.lang.compiler.program import Program
from starkware.cairo.lang.compiler.scoped_name import ScopedName
from starkware.cairo.lang.vm.cairo_runner import CairoRunner
from starkware.cairo.lang.vm.memory_dict import MemoryDict
from starkware.cairo.lang.vm.memory_segments import FIRST_MEMORY_ADDR as PROGRAM_BASE
from starkware.cairo.lang.vm.security import verify_secure_runner
from starkware.cairo.lang.vm.utils import RunResources
from starkware.cairo.lang.vm.vm import VirtualMachine
from starkware.starknet.compiler.starknet_pass_manager import starknet_pass_manager

from utils.profiling import profile_from_trace
from utils.serde import Serde

logging.getLogger("asyncio").setLevel(logging.ERROR)
logger = logging.getLogger()


def pytest_addoption(parser):
    parser.addoption(
        "--profile-cairo",
        action="store_true",
        default=False,
        help="compute and dump TracerData for the VM runner: True or False",
    )


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def cairo_compile(path):
    module_reader = get_module_reader(cairo_path=["src"])

    pass_manager = starknet_pass_manager(
        prime=DEFAULT_PRIME,
        read_module=module_reader.read,
        disable_hint_validation=True,
    )

    return compile_cairo(
        Path(path).read_text(),
        pass_manager=pass_manager,
        debug_info=True,
    )


@pytest.fixture(scope="module")
def cairo_run(request) -> list:
    """
    Run the cairo program corresponding to the python test file at a given entrypoint with given program inputs as kwargs.
    Returns the output of the cairo program put in the output memory segment.

    When --profile-cairo is passed, the cairo program is run with the tracer enabled and the resulting trace is dumped.

    Logic is mainly taken from starkware.cairo.lang.vm.cairo_run with minor updates like the addition of the output segment.
    """
    cairo_file = Path(request.node.fspath).with_suffix(".cairo")
    if not cairo_file.exists():
        raise ValueError(f"Missing cairo file: {cairo_file}")

    start = perf_counter()
    cairo_program = cairo_compile(cairo_file)
    stop = perf_counter()
    logger.info(f"{cairo_file} compiled in {stop - start:.2f}s")

    def _run(entrypoint, *args, **kwargs):
        # ============================================================================
        # STEP 1: SELECT PROGRAM AND PREPARE ENTRYPOINT METADATA
        # - Rationale: We need to determine which program contains the entrypoint (main or test)
        #   and extract its argument/return type metadata for type conversion and execution.
        # ============================================================================
        _builtins, _implicit_args, _args, return_data_types = build_entrypoint(
            cairo_program, entrypoint, get_main_path(cairo_file), lambda _x: None
        )

        # ============================================================================
        # STEP 2: INITIALIZE RUNNER AND MEMORY ENVIRONMENT
        # - Rationale: Set up the CairoRunner with the program, layout, and memory.
        # We append a "jmp rel 0" instruction to enable looping at the end of the program, so that when ran in proof mode,
        # the number of executed steps can always be a power of two.
        # ============================================================================
        cairo_program.data = cairo_program.data + [0x10780017FFF7FFF, 0]  # jmp rel 0
        memory = MemoryDict()
        runner = CairoRunner(
            program=cairo_program,
            layout="starknet_with_keccak",
            memory=memory,
            proof_mode=False,
            allow_missing_builtins=False,
        )
        dict_manager = DictManager()
        serde = Serde(runner)
        runner.program_base = runner.segments.add()
        runner.execution_base = runner.segments.add()
        for builtin_runner in runner.builtin_runners.values():
            builtin_runner.initialize_segments(runner)

        # ============================================================================
        # STEP 3: BUILD INITIAL STACK WITH BUILTINS AND ARGUMENTS
        # - Rationale: Construct the stack with unused builtins (in proof mode - all builtins of the
        #   layout must be present) and all input arguments (implicit and explicit). This prepares the
        #   VM's execution context.
        # ============================================================================
        stack = []
        for builtin_arg in _builtins:
            builtin_runner = runner.builtin_runners.get(
                builtin_arg.replace("_ptr", "_builtin")
            )
            if builtin_runner is None:
                raise ValueError(f"Builtin runner {builtin_arg} not found")
            stack.extend(builtin_runner.initial_stack())

        for i, (arg_name, _python_type) in enumerate(
            [(k, v["python_type"]) for k, v in {**_implicit_args, **_args}.items()]
        ):
            arg_value = kwargs[arg_name] if arg_name in kwargs else args[i]
            stack.append(runner.segments.gen_arg(arg_value))

        # ============================================================================
        # STEP 4: SET UP EXECUTION CONTEXT AND LOAD MEMORY
        # - Rationale: Finalize the stack with return pointers, set initial VM registers,
        #   and load program/data into memory to start execution.
        # - Add the dummy last fp and pc to the public memory, so that the verifier can enforce
        #   [fp - 2] = fp.
        # ============================================================================
        return_fp = runner.execution_base + 2
        end = runner.program_base + len(runner.program.data) - 2  # Points to jmp rel 0
        stack = [return_fp, end] + stack + [return_fp, end]
        # All elements of the input stack are added to the execution public memory - required for proof mode
        runner.execution_public_memory = list(range(len(stack)))
        # Start the run at the offset of the entrypoint
        runner.initial_pc = runner.program_base + cairo_program.get_label(entrypoint)
        # Load the program into memory
        runner.load_data(runner.program_base, runner.program.data)
        runner.load_data(runner.execution_base, stack)  # Load the stack into memory
        # Set the initial frame pointer and argument pointer to the end of the stack
        runner.initial_fp = runner.initial_ap = runner.execution_base + len(stack)
        runner.initialize_zero_segment()

        # ============================================================================
        # STEP 5: CONFIGURE VM AND EXECUTE PROGRAM
        # - Rationale: Initialize the VM with hints, set execution limits, and run until the
        #   end address. Catch exceptions for debugging or coverage analysis.
        # ============================================================================
        runner.initialize_vm(
            hint_locals={
                "program_input": kwargs,
                "builtin_runners": runner.builtin_runners,
                "__dict_manager": dict_manager,
                "dict_manager": dict_manager,
                "serde": serde,
            },
            static_locals={
                "debug_info": debug_info(cairo_program),
            },
            vm_class=VirtualMachine,
        )
        if not isinstance(runner.vm, VirtualMachine):
            raise ValueError("VM is not a VirtualMachine")

        max_steps = 1_000_000_000
        if hasattr(
            request.node, "get_closest_marker"
        ) and request.node.get_closest_marker("max_steps"):
            max_steps = request.node.get_closest_marker("max_steps").args[0]
        run_resources = RunResources(n_steps=max_steps)
        try:
            runner.run_until_pc(end, run_resources)
        except Exception as e:
            runner.end_run(disable_trace_padding=False)
            runner.relocate()
            trace = pl.DataFrame(
                [{"pc": x.pc, "ap": x.ap, "fp": x.fp} for x in runner.relocated_trace]
            )
            raise e

        # ============================================================================
        # STEP 6: PROCESS RETURN VALUES AND FINALIZE EXECUTION
        # - `end_run`: relocates all memory segments and ensures that in proof mode, the number of executed steps is a power of two
        # - Once the run is over, we extract return data using serde, update the public memory in proof mode by adding the return data offsets to the public memory
        #   and performs security checks
        # ============================================================================
        runner.end_run(disable_trace_padding=False)
        cumulative_retdata_offsets = serde.get_offsets(return_data_types)
        first_return_data_offset = (
            cumulative_retdata_offsets[0] if cumulative_retdata_offsets else 0
        )
        if not isinstance(first_return_data_offset, int):
            raise ValueError("First return data offset is not an int")

        # Pointer to the first "builtin" - which are not considered as part of the return data
        pointer = runner.vm.run_context.ap - first_return_data_offset
        for arg in _builtins[::-1]:
            builtin_runner = runner.builtin_runners.get(arg.replace("_ptr", "_builtin"))
            if builtin_runner:
                pointer = builtin_runner.final_stack(runner, pointer)
            else:
                pointer -= 1
        verify_secure_runner(runner)
        runner.relocate()

        # ============================================================================
        # STEP 7: GENERATE OUTPUT FILES AND TRACE (IF REQUESTED)
        # ============================================================================
        trace = pl.DataFrame(
            [{"pc": x.pc, "ap": x.ap, "fp": x.fp} for x in runner.relocated_trace]
        )

        # Create a unique output stem for the given test by using the test file name, the entrypoint and the kwargs
        displayed_args = ""
        if kwargs:
            try:
                displayed_args = json.dumps(kwargs)
            except TypeError as e:
                logger.debug(f"Failed to serialize kwargs: {e}")
        output_stem = str(
            request.node.path.parent
            / f"{request.node.path.stem}_{entrypoint}_{displayed_args}"
        )
        # File names cannot be longer than 255 characters on Unix so we slice the base stem and happen a unique suffix
        # Timestamp is used to avoid collisions when running the same test multiple times and to allow sorting by time
        output_stem = Path(
            f"{output_stem[:160]}_{int(time_ns())}_{md5(output_stem.encode()).digest().hex()[:8]}"
        )

        if request.config.getoption("profile_cairo"):
            stats, prof_dict = profile_from_trace(
                program=cairo_program, trace=trace, program_base=PROGRAM_BASE
            )
            stats = stats[
                "scope", "primitive_call", "total_call", "total_cost", "cumulative_cost"
            ].sort("cumulative_cost", descending=True)
            logger.info(stats)
            stats.write_csv(output_stem.with_suffix(".csv"))
            marshal.dump(prof_dict, open(output_stem.with_suffix(".prof"), "wb"))

        # ============================================================================
        # STEP 8: SERIALIZE AND RETURN OUTPUT
        #   For test purposes.
        # - Rationale: Convert Cairo return values to Python types, handle exceptions,
        #   and format the final output for the caller.
        # ============================================================================
        unfiltered_output = [
            serde.serialize(return_data_type)
            for offset, return_data_type in zip(
                cumulative_retdata_offsets, return_data_types, strict=False
            )
        ]
        function_output = serde.filter_no_error_flag(unfiltered_output)
        exceptions = [
            val
            for val in flatten(function_output)
            if hasattr(val, "__class__") and issubclass(val.__class__, Exception)
        ]
        if exceptions:
            raise exceptions[0]

        final_output = function_output
        return final_output[0] if len(final_output) == 1 else final_output

    return _run


def resolve_main_path(main_path: Tuple[str, ...]):
    """
    Resolve Cairo type paths for proper type system integration.

    It ensures types defined in __main__ (when the test file is the main file)
    are properly mapped to their actual module paths for serialization/deserialization.
    """

    def _factory(cairo_type: CairoType):
        if isinstance(cairo_type, TypeStruct):
            full_path = cairo_type.scope.path
            if "__main__" in full_path:
                full_path = main_path + full_path[full_path.index("__main__") + 1 :]
                cairo_type.scope = ScopedName(full_path)
        return cairo_type

    return _factory


def build_entrypoint(
    cairo_program: Program,
    entrypoint: str,
    main_path: Tuple[str, ...],
    to_python_type: Callable,
):
    implicit_args = cairo_program.get_identifier(
        f"{entrypoint}.ImplicitArgs", StructDefinition
    ).members

    # Split implicit args into builtins and other implicit args
    _builtins = [
        k
        for k in implicit_args.keys()
        if any(builtin in k.replace("_ptr", "") for builtin in ALL_BUILTINS)
    ]

    _implicit_args = {
        k: {
            "python_type": to_python_type(resolve_main_path(main_path)(v.cairo_type)),
            "cairo_type": v.cairo_type,
        }
        for k, v in implicit_args.items()
        if not any(builtin in k.replace("_ptr", "") for builtin in ALL_BUILTINS)
    }

    entrypoint_args = cairo_program.get_identifier(
        f"{entrypoint}.Args", StructDefinition
    ).members

    _args = {
        k: {
            "python_type": to_python_type(resolve_main_path(main_path)(v.cairo_type)),
            "cairo_type": v.cairo_type,
        }
        for k, v in entrypoint_args.items()
    }

    explicit_return_data = cairo_program.get_identifier(
        f"{entrypoint}.Return", TypeDefinition
    ).cairo_type

    return_data_types = [
        *(arg["cairo_type"] for arg in _implicit_args.values()),
        # Filter for the empty tuple return type
        *(
            [explicit_return_data]
            if not (
                isinstance(explicit_return_data, TypeTuple)
                and len(explicit_return_data.members) == 0
            )
            else []
        ),
    ]

    # Fix builtins runner based on the implicit args since the compiler doesn't find them
    cairo_program.builtins = [
        builtin
        for builtin in ALL_BUILTINS
        if builtin in [arg.replace("_ptr", "") for arg in _builtins]
    ]

    return _builtins, _implicit_args, _args, return_data_types


def get_main_path(cairo_file: Optional[Path]) -> Optional[Tuple[str, ...]]:
    """
    Resolve the __main__ part of the cairo scope path.
    """
    if not cairo_file:
        return None
    return tuple(
        "/".join(cairo_file.relative_to(Path.cwd()).with_suffix("").parts)
        .replace("cairo/", "")
        .split("/")
    )


def debug_info(program: Program):
    def _debug_info(pc):
        if program.debug_info is None:
            raise ValueError("Program debug info is not set")

        if (
            instruction_location := program.debug_info.instruction_locations.get(
                pc.offset
            )
        ) is None:
            raise ValueError("Instruction location not found")

        print(instruction_location.inst.to_string_with_content(""))

    return _debug_info


def flatten(data):
    result = []

    def _flatten(item):
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes, bytearray)):
            for sub_item in item:
                _flatten(sub_item)
        else:
            result.append(item)

    _flatten(data)
    return result
