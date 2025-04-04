
from starkware.cairo.common.math_cmp import is_not_zero

// Sometimes, conditionals can be avoided by using an expression that
// - maps valid inputs to 1,
// - and/or maps invalid inputs to 0.
// For instance (row - 2) * (row - 4) is 0 only when row is 2 or 4.

// Use this trick to rewrite functions without "if" conditions
// Note: This helps to avoid dealing with revoked references.

// I AM NOT DONE

func is_binary_if(x: felt) -> felt {
    if (x == 0) {
        return 1;
    }
    if (x == 1) {
        return 1;
    }
    return 0;
}

// TODO: Return the right value to mimick the behavior of is_binary_if

func is_binary_no_if(x: felt) -> felt {
    // FILL ME
    return res;
}

// TODO: Fix the function so that
//  - it returns the string 'cool' if x is 1337, 69420, 42
//  - it returns 'meh' on any other input

func is_cool(x: felt) -> felt {
    // FILL ME
    return res;
}

// Do not change the test
func test_is_binary() {
    let eval_if = is_binary_if(0);
    let eval_no_if = is_binary_no_if(0);
    assert (eval_if, eval_no_if) = (1, 1);

    let eval_if = is_binary_if(1);
    let eval_no_if = is_binary_no_if(1);
    assert (eval_if, eval_no_if) = (1, 1);

    let eval_if = is_binary_if(13);
    let eval_no_if = is_binary_no_if(37);
    assert (eval_if, eval_no_if) = (0, 0);
    return ();
}

func test_is_cool() {
    let is_1337_cool = is_cool(1337);
    let is_69420_cool = is_cool(69420);
    let is_42_cool = is_cool(42);
    let is_0_cool = is_cool(0);
    let is_911_cool = is_cool(911);
    let results = ('cool', 'cool', 'cool', 'meh', 'meh');
    assert (is_1337_cool, is_69420_cool, is_42_cool, is_0_cool, is_911_cool) = results;
    return ();
}
