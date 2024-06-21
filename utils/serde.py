from starkware.cairo.lang.compiler.ast.cairo_types import (
    TypeFelt,
    TypePointer,
    TypeStruct,
    TypeTuple,
)
from starkware.cairo.lang.compiler.identifier_definition import StructDefinition
from starkware.cairo.lang.compiler.identifier_manager import MissingIdentifierError


class Serde:
    def __init__(self, runner):
        self.runner = runner
        self.memory = runner.segments.memory

    def get_identifier(self, struct_name, expected_type):
        identifiers = [
            value
            for key, value in self.runner.program.identifiers.as_dict().items()
            if struct_name in str(key)
            and isinstance(value, expected_type)
            and struct_name.split(".")[-1] == str(key).split(".")[-1]
        ]
        if len(identifiers) != 1:
            raise ValueError(
                f"Expected one struct named {struct_name}, found {identifiers}"
            )
        return identifiers[0]

    def serialize_list(self, segment_ptr, item_scope=None, list_len=None):
        item_identifier = (
            self.get_identifier(item_scope, StructDefinition)
            if item_scope is not None
            else None
        )
        item_type = (
            TypeStruct(item_identifier.full_name)
            if item_scope is not None
            else TypeFelt()
        )
        item_size = item_identifier.size if item_identifier is not None else 1
        list_len = (
            list_len * item_size
            if list_len is not None
            else self.runner.segments.get_segment_size(segment_ptr.segment_index)
        )
        output = []
        for i in range(0, list_len, item_size):
            try:
                output.append(self._serialize(item_type, segment_ptr + i))
            # Because there is no way to know for sure the length of the list, we stop when we
            # encounter an error.
            # trunk-ignore(ruff/E722)
            except:
                break
        return output

    def serialize_dict(self, dict_ptr, value_scope=None):
        dict_size = self.runner.segments.get_segment_size(dict_ptr.segment_index)
        output = {}
        value_scope = (
            self.get_identifier(value_scope, StructDefinition).full_name
            if value_scope is not None
            else None
        )
        for dict_index in range(0, dict_size, 3):
            key = self.memory.get(dict_ptr + dict_index)
            value_ptr = self.memory.get(dict_ptr + dict_index + 2)
            if value_scope is None:
                output[key] = value_ptr
            else:
                output[key] = (
                    self.serialize_scope(value_scope, value_ptr)
                    if value_ptr != 0
                    else None
                )
        return output

    def serialize_pointers(self, name, ptr):
        members = self.get_identifier(name, StructDefinition).members
        output = {}
        for name, member in members.items():
            member_ptr = self.memory.get(ptr + member.offset)
            if member_ptr == 0 and isinstance(member.cairo_type, TypePointer):
                member_ptr = None
            output[name] = member_ptr
        return output

    def serialize_struct(self, name, ptr):
        if ptr is None:
            return None
        members = self.get_identifier(name, StructDefinition).members
        return {
            name: self._serialize(member.cairo_type, ptr + member.offset)
            for name, member in members.items()
        }

    def serialize_uint256(self, ptr):
        raw = self.serialize_pointers("Uint256", ptr)
        return hex(raw["low"] + raw["high"] * 2**128)

    def serialize_scope(self, scope, scope_ptr):
        if scope.path[-1] == "Uint256":
            return self.serialize_uint256(scope_ptr)
        try:
            return self.serialize_struct(str(scope), scope_ptr)
        except MissingIdentifierError:
            return scope_ptr

    def _serialize(self, cairo_type, ptr, length=1):
        if isinstance(cairo_type, TypePointer):
            # A pointer can be a pointer to one single struct or to the beginning of a list of structs.
            # As such, every pointer is considered a list of structs, with length 1 or more.
            pointee = self.memory.get(ptr)
            # Edge case: 0 pointers are not pointer but no data
            if pointee == 0:
                return None
            if isinstance(cairo_type.pointee, TypeFelt):
                return self.serialize_list(pointee)
            serialized = self.serialize_list(
                pointee, str(cairo_type.pointee.scope), list_len=length
            )
            if len(serialized) == 1:
                return serialized[0]
            return serialized
        if isinstance(cairo_type, TypeTuple):
            return [
                self._serialize(m.typ, ptr + i)
                for i, m in enumerate(cairo_type.members)
            ]
        if isinstance(cairo_type, TypeFelt):
            return self.memory.get(ptr)
        if isinstance(cairo_type, TypeStruct):
            return self.serialize_scope(cairo_type.scope, ptr)
        raise ValueError(f"Unknown type {cairo_type}")

    def serialize(self, cairo_type):
        if hasattr(cairo_type, "members"):
            shift = len(cairo_type.members)
        else:
            try:
                identifier = self.get_identifier(
                    str(cairo_type.scope), StructDefinition
                )
                shift = len(identifier.members)
            except (ValueError, AttributeError):
                shift = 1
        return self._serialize(cairo_type, self.runner.vm.run_context.ap - shift, shift)
