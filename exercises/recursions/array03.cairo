%lang starknet
from starkware.cairo.common.math_cmp import is_le
from starkware.cairo.common.alloc import alloc

// TODO
// Scan through the array elements from first to last
// Return 1 if elements of the array are in increasing order.
// Return 0 otherwise
func is_increasing{range_check_ptr: felt}(array_len: felt, array: felt*) -> felt {
    if (array_len == 0) {
        return 1;
    }
    if (array_len == 1) {
        return 1;
    }
    let curr_value = 0;
    let next_value = 0;

    // Do not modify these lines
    let is_sorted = is_le(curr_value, next_value);
    if (is_sorted == 1) {
        return is_increasing(array_len - 1, array + 1);
    }
    return 0;
}

// TODO
// Scan through the array elements from last to first
// Return 1 if elements of the array are in decreasing order.
// Return 0 otherwise
func is_decreasing{range_check_ptr: felt}(array_len: felt, array: felt*) -> felt {
    // FILL ME

    // Do not modify this line
    let (is_sorted) = is_le(curr_value, next_value);

    if (is_sorted == 1) {
        return is_decreasing(array, array_len);
    }
    return 0;
}

// TODO
// Use recursion to reverse array in rev_array
// Assume rev_array is already allocated
func reverse(array_len: felt, array: felt*, rev_array: felt*) {
    // FILL ME
    return ();
}

func test__is_increasing{range_check_ptr}() -> felt {
    alloc_locals;
    local array_len;
    let (array) = alloc();
    %{
        ids.array_len = len(program_input["array"])
        segments.write_arg(ids.array, program_input["array"])
    %}
    let result = is_increasing(array_len, array);
    return result;
}

func test__is_decreasing{range_check_ptr}() -> felt {
    alloc_locals;
    local array_len;
    let (array) = alloc();
    %{
        ids.array_len = len(program_input["array"])
        segments.write_arg(ids.array, program_input["array"])
    %}
    let result = is_decreasing(array_len, array);
    return result;
}

func test__reverse() -> felt* {
    alloc_locals;
    local array_len;
    let (array) = alloc();
    let (rev_array) = alloc();
    %{
        ids.array_len = len(program_input["array"])
        segments.write_arg(ids.array, program_input["array"])
    %}
    reverse(array_len, array, rev_array);
    return rev_array;
}
