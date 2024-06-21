// Implicit arguments are passed down to any subsequent function calls that would require them.
// Make good usage of this feature to pass this exercise!

// I AM NOT DONE

// TODO: fix the "child_function_1" and "child_function_2" signatures to make the test pass

// Do not change the function signature
func parent_function{a, b}() -> felt{
    // Do not change the function body
    alloc_locals;
    let intermediate_result_1 = child_function_1();
    let intermediate_result_2 = child_function_2();
    return intermediate_result_1 + intermediate_result_2;
}

func child_function_1() -> felt{
    // Do not change the function body
    return 2 * a;
}

func child_function_2() -> felt{
    // Do not change the function body
    return b + 3;
}

func test__sum()-> felt{
    alloc_locals;
    local a;
    local b;
    %{
        ids.a = program_input["a"]
        ids.b = program_input["b"]
    %}
    with a, b{
        let result = parent_function();
    }

    return result;
}
