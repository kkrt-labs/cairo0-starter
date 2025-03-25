%lang starknet

from starkware.cairo.common.math import assert_lt_felt

// Felts use prime number property to ensure (x / y) * y = x is always true.
// It is still possible to manage negative numbers thanks to field element properties.
// Exercice resources: https://docs.cairo-lang.org/cairozero/hello_cairo/intro.html#the-primitive-type-field-element-felt

// I AM NOT DONE

// TODO
// Set the value of x (in the hint) to verify the test
func solve() -> (x : felt){
    tempvar x;
    %{ ids.x = -17 %}  // Change only this line to make the test pass
    return (x=x);
}

// Do not change the test
func test_solve{}(){
    let (x) = solve();
    assert x = -17;
    return();
}
