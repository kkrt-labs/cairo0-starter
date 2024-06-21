%builtins range_check bitwise

from starkware.cairo.common.math import assert_le, assert_nn
from starkware.cairo.common.math_cmp import is_not_zero
from starkware.cairo.common.bitwise import bitwise_and, bitwise_xor, bitwise_or
from starkware.cairo.common.cairo_builtins import BitwiseBuiltin
from starkware.cairo.common.pow import pow

// While operations like addition, multiplication and divisions are native for felts,
// bit operations are more difficult to implement for felt.
// The bitwise builtin allows computing logical operations such as XOR, AND and OR on 251-bit felts.

// Resources:
// - https://github.com/starkware-libs/cairo-lang/blob/master/src/starkware/cairo/common/bitwise.cairo
// - https://github.com/starkware-libs/cairo-lang/blob/master/src/starkware/cairo/common/cairo_builtins.cairo#L17

// I AM NOT DONE

// TODO: Use a bitwise operation to return the n-th bit of the value parameter

func get_nth_bit{range_check_ptr, bitwise_ptr: BitwiseBuiltin*}() -> felt {
    alloc_locals;
    local value;
    local n;
    %{
        ids.value = program_input["value"]
        ids.n = program_input["n"]
    %}
    // FILL ME
    let (pow2n) = pow(2, n);
    let (and_val) = bitwise_and(value, pow2n);
    let res = is_not_zero(and_val);
    return res;
}

// TODO: Use a bitwise operation to set the n-th bit of the value parameter to 1

func set_nth_bit{bitwise_ptr : BitwiseBuiltin*, range_check_ptr : felt}() -> felt{
    alloc_locals;
    local value;
    local n;
    %{
        ids.value = program_input["value"]
        ids.n = program_input["n"]
    %}
    // FILL ME
    let (pow2n) = pow(2, n);
    let (res) = bitwise_or(value, pow2n);
    return res;
}

// TODO: Use a bitwise operation to toggle the n-th bit of the value parameter

func toggle_nth_bit{bitwise_ptr : BitwiseBuiltin*, range_check_ptr : felt}() -> felt{
    alloc_locals;
    local value;
    local n;
    %{
        ids.value = program_input["value"]
        ids.n = program_input["n"]
    %}
    // FILL ME
   let (pow2n) = pow(2, n);
   let (res) = bitwise_xor(value, pow2n);
    return res;
}

// Let's write a unique function that combines all the functions above.
// This function should use the bitwise_ptr explicitly.
// In particular, do not use any of the functions above.

// TODO: Write a function that takes as argument
//        - a felt `op` in ['get', 'set', 'toggle'],
//        - felts `value` and `n`,
//       and returns the result of the operation applied to `n`-th bit of value.
// Make sure
//   - the argument `n` is within the correct bitwise bounds,
//   - the `op` argument is correct.

func op_nth_bit{bitwise_ptr : BitwiseBuiltin*, range_check_ptr : felt}() -> felt{
    alloc_locals;
    local op;
    local value;
    local n;

    %{
        ids.op = program_input["op"]
        ids.value = program_input["value"]
        ids.n = program_input["n"]
    %}

    // Assert op is correct
    assert 0 = (op - 'get') * (op - 'set') * (op - 'toggle');

    with_attr error_message("Bad bitwise bounds"){
        // Assert n is within bounds
           assert_nn(n);
           assert_le(n, 250);
    }

    // Compute the operation
    // Don't forget to advance bitwise_ptr
    let (pow2n) = pow(2, n);
    assert bitwise_ptr.x = value;
    assert bitwise_ptr.y = pow2n;

    local res;
    if (op == 'get'){
        let tmp = is_not_zero(bitwise_ptr.x_and_y);
        assert res = tmp;
    }else{
        if (op == 'set'){
            assert res = bitwise_ptr.x_or_y;
        }else{
            // op == 'toggle'
            assert res = bitwise_ptr.x_xor_y;
        }
    }

    let bitwise_ptr = bitwise_ptr + BitwiseBuiltin.SIZE;

    return res;
}
