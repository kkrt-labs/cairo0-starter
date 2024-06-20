%lang starknet

// I AM NOT DONE

// Ressources
// https://www.cairo-lang.org/docs/how_cairo_works/cairo_intro.html#registers
// https://www.cairo-lang.org/docs/how_cairo_works/functions.html#function-arguments-and-return-values

// TODO
// Rewrite this function body in a high level syntax
func ret_42() -> felt{
    // [ap] = 42; ap++
    // ret
    return 42;
}

// TODO
// Rewrite this function body in a low level syntax, using registers
func ret_0_and_1() -> (zero : felt, one : felt){
    // return (0, 1);
    [ap] = 0, ap++;
    [ap] = 1, ap++;
    ret;
}
