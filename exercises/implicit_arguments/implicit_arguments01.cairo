// Functions can take implicit arguments. You might have already encountered this with
// syscall_ptr: felt* for example.

// I AM NOT DONE

// TODO: fix the "implicit_sum" signature to make the test pass

func implicit_sum() -> felt{
    return a + b;
}

// Do not change the test
func test__sum() -> felt{
    alloc_locals;
    local a;
    local b;
    %{
        ids.a = program_input["a"]
        ids.b = program_input["b"]
    %}
    let sum = implicit_sum{a=a, b=b}();

    return sum;
}
