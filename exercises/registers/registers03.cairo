from starkware.cairo.common.math_cmp import is_le

// I AM NOT DONE

// TODO
// Rewrite those functions with a high level syntax
func sum_array(array_len: felt, array: felt*) -> felt {
    // [ap] = [fp - 4], ap++;
    // [ap] = [fp - 3], ap++;
    // [ap] = 0, ap++;
    // call rec_sum_array;
    // ret;

    return rec_sum_array(array_len, array, 0);
}

func rec_sum_array(array_len: felt, array: felt*, sum: felt) -> felt {
    // jmp continue if [fp - 5] != 0;

    // stop:
    // [ap] = [fp - 3], ap++;
    // jmp done;

    // continue:
    // [ap] = [[fp - 4]], ap++;
    // [ap] = [fp - 5] - 1, ap++;
    // [ap] = [fp - 4] + 1, ap++;
    // [ap] = [ap - 3] + [fp - 3], ap++;
    // call rec_sum_array;

    // done:
    // ret;
    if (array_len == 0) {
        return sum;
    }

    return rec_sum_array(array_len - 1, array + 1, sum + array[0]);
}

// TODO
// Rewrite this function with a low level syntax
// It's possible to do it with only registers, labels and conditional jump. No reference or localvar
func max{range_check_ptr}(a: felt, b: felt) -> felt {
    // let (res) = is_le(a, b);
    // if res == 1:
    //     return (b);
    // else:
    //     return (a);
    // }

    // Push arguments to the stack
    [ap] = [fp - 5], ap++;  // range_check_ptr
    [ap] = [fp - 4], ap++;  // a
    [ap] = [fp - 3], ap++;  // b

    // This call will return two values
    // 1) the updated range_check_ptr
    // 2) 0 or 1 depending on which of a and b is greater
    call is_le;

    // Push return values to the stack
    // There is two of them to push: range_check_ptr and max

    // Push the first one, the updated range_check_ptr, onto the stack
    [ap] = [ap - 2], ap++;

    // Conditional jump
    // The following blocks are an assembly level equivalent of the if/else pattern
    jmp b_is_more if [ap - 2] != 0;  // here [ap-2] is the second value returned by is_le, our boolean

    // Push either a or b to the stack
    a_is_more:
    [ap] = [fp - 4], ap++;
    jmp done;

    b_is_more:
    [ap] = [fp - 3], ap++;

    done:
    ret;
}

// TESTS #

from starkware.cairo.common.alloc import alloc

func test_max{range_check_ptr}() -> felt {
    alloc_locals;
    local a;
    local b;
    %{
        ids.a = program_input["a"]
        ids.b = program_input["b"]
    %}
    let max_ = max(a, b);
    return max_;
}

func test_sum() -> felt {
    alloc_locals;
    let (array) = alloc();
    local array_len;
    %{
        ids.array_len = len(program_input["array"])
        segments.write_arg(ids.array, program_input["array"])
    %}

    let s = sum_array(array_len, array);
    return s;
}
