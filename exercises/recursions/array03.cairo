%lang starknet
from starkware.cairo.common.math_cmp import is_le
from starkware.cairo.common.alloc import alloc

func is_increasing{range_check_ptr : felt}(array_len : felt, array : felt*) -> felt{
    if (array_len == 0){
        return 1;
    }
    if (array_len == 1){
        return 1;
    }
    let curr_value = [array];
    let next_value = [array + 1];
    let is_sorted = is_le(curr_value, next_value);
    if (is_sorted == 1){
        return is_increasing(array_len - 1, array + 1);
    }
    return 0;
}

func is_decreasing{range_check_ptr : felt}(array_len : felt, array : felt*) -> felt{
    if (array_len == 0){
        return 1;
    }
    if (array_len == 1){
        return 1;
    }
    let curr_value = [array + array_len - 1];
    let next_value = [array + array_len - 2];
    let is_sorted = is_le(curr_value, next_value);
    if (is_sorted == 1){
        return is_decreasing(array_len - 1, array);
    }
    return 0;
}

func reverse(array_len : felt, array : felt*, rev_array : felt*){
    if (array_len == 0){
        return ();
    }
    assert [rev_array] = [array + array_len - 1];
    return reverse(array_len - 1, array, rev_array + 1);
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
