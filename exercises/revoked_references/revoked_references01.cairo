// References in Cairo are like aliases to specific memory cells pointed by ap

// I AM NOT DONE

// TODO: complete the bar function to make the test pass
// You will encounter a "revoked reference" error
// https://docs.cairo-lang.org/cairozero/how_cairo_works/consts.html#revoked-references

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.cairo.common.hash import hash2

func foo(n) {
    if (n == 0) {
        return ();
    }
    foo(n=n - 1);
    return ();
}

func bar{hash_ptr: HashBuiltin*}() {
    hash2(1, 2);  // Do not change
    foo(3);  // Do not change

    // Insert something here to make the test pass.
    // hint: how can you store something that will not be ap-dependant?

    hash2(3, 4);  // Do not change
    return ();  // Do not change
}

// Do not change the test
func test_bar{pedersen_ptr: HashBuiltin*}() {
    bar{hash_ptr=pedersen_ptr}();

    return ();
}
