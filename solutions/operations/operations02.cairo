%lang starknet

from starkware.cairo.common.math import assert_lt_felt, assert_not_zero

// Felts use prime number property to ensure (x / y) * y = x is always true.
// Since floats are not supported, this can lead to get surprising results.
// Exercice resources: https://docs.cairo-lang.org/hello_cairo/intro.html#the-primitive-type-field-element-felt

// I AM NOT DONE

// TODO
// Find a number X which satisfy A / X > A with X in range ]0 ; 100]
func solve(a : felt) -> felt{
    // TO FILL
    let x = 53;
    return x;
}

// Do not change the test
func test__solve{range_check_ptr}(){
    let a = 347092984475551631116800;
    let x = solve(a=a);
    assert_not_zero(x);
    assert_lt_felt(x, 101);
    assert_lt_felt(a, a / x);
    return();
}
