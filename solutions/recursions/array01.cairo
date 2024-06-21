

// Arrays can be passed as function arguments in the form of a pointer and a length.

// I AM NOT DONE

// TODO: write the "contains" function body that returns 1 if the haystack contains the needle and 0 otherwise.

from starkware.cairo.common.alloc import alloc

func contains(needle : felt, haystack_len : felt, haystack : felt*) -> felt{
    if (haystack_len == 0) {
        return 0;
    }

    if (needle == [haystack]) {
        return 1;
    }

    return contains(needle, haystack_len - 1, haystack + 1);
}

func test__contains() -> felt{
    alloc_locals;
    local needle;
    local haystack_len;
    let (haystack) = alloc();

    %{
        ids.needle = program_input["needle"]
        ids.haystack_len = len(program_input["haystack"])
        segments.write_arg(ids.haystack, program_input["haystack"])
    %}

    return contains(needle, haystack_len, haystack);
}
