%lang starknet

// Felts supports basic math operations.
// High level syntax allows one-line multiple operations while low level syntax doesn't.
// Exercice source: https://www.cairo-lang.org/docs/how_cairo_works/cairo_intro.html#field-elements

// I AM NOT DONE

// TODO
// Write this function body in a high level syntax
func poly_high_level(x: felt) -> felt {
    // return x³ + 23x² + 45x + 67 according to x
    tempvar x3 = x * x * x;
    tempvar x2 = x * x;
    tempvar res = x3 + 23 * x2 + 45 * x + 67;
    return res;  // Do not change
}

// TODO
// Write this function body in a low level syntax (result must be stored in [ap - 1] before ret)
func poly_low_level(x: felt) -> felt {
    // return x³ + 23x² + 45x + 67 according to x
    [ap] = x * x, ap++;
    [ap] = [ap - 1] * x, ap++;
    [ap] = [ap - 2] * 23, ap++;
    [ap] = x * 45, ap++;
    [ap] = [ap - 1] + 67, ap++;
    [ap] = [ap - 1] + [ap - 3], ap++;
    [ap] = [ap - 1] + [ap - 5], ap++;
    ret;  // Do not change
}

// Do not change the test
func test_poly_low_level() -> felt {
    alloc_locals;
    local x;
    %{ ids.x = program_input["x"] %}
    let res = poly_low_level(x=x);
    return res;
}

func test_poly_high_level() -> felt {
    alloc_locals;
    local x;
    %{ ids.x = program_input["x"] %}
    let res = poly_high_level(x=x);
    return res;
}
