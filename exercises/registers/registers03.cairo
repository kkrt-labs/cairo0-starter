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
}

// TODO
// Rewrite this function with a low level syntax
// It's possible to do it with only registers, labels and conditional jump. No reference or localvar
func max{range_check_ptr}(a: felt, b: felt) -> felt {
    // let (res) = is_le(a, b);
    // if res == 1:
    //     return b;
    // else:
    //     return a;
    // }
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
