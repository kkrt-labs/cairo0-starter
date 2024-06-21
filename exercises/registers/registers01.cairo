%lang starknet

// I AM NOT DONE

// Resource
// https://www.cairo-lang.org/docs/how_cairo_works/functions.html#function-arguments-and-return-values

// TODO
// Rewrite this function with a high level syntax
func assert_is_42(){
    alloc_locals;
    local n;
    %{
        ids.n = program_input["n"]
    %}
    // REWRITE ME
    // [ap - 3] = 42
    // ret
}

// TODO
// Rewrite this function with a low level syntax, using registers
func sum(a : felt, b : felt) -> felt{
    // REWRITE ME
    // return (a + b)
}

func test_sum() -> felt {
    alloc_locals;
    local a;
    local b;
    %{
        ids.a = program_input["a"]
        ids.b = program_input["b"]
    %}
    let s = sum(a, b);
    return s;
}
