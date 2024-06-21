// Functions can take arguments and return results

// I AM NOT DONE

// TODO: make the test pass!

func takes_two_arguments_and_returns_one() -> felt {
    return a + b;  // Do not change
}

// You could be tempted to change the test to make it pass, but don't?
func test_sum() -> felt {
    alloc_locals;
    local a;
    local b;
    %{
        ids.a = program_input["a"]
        ids.b = program_input["b"]
    %}
    let sum = takes_two_arguments_and_returns_one(a, b);
    return sum;
}
