%lang starknet

from starkware.cairo.common.math_cmp import is_not_zero

struct Point {
    x : felt,
    y : felt,
    z : felt,
}

func contains_origin{range_check_ptr : felt}(len_points : felt, points : Point*) -> felt {
    // FILL ME
}

// TESTS
from starkware.cairo.common.alloc import alloc

func test_contains_origin{range_check_ptr : felt}() {
    alloc_locals;
    let (local false_array : Point*) = alloc();
    assert false_array[0] = Point(1, 2, 3);
    assert false_array[1] = Point(2, 2, 2);
    assert false_array[2] = Point(42, 27, 11);
    let res = contains_origin(3, false_array);
    assert res = 0;

    let (local true_array : Point*) = alloc();
    assert true_array[0] = Point(1, 2, 3);
    assert true_array[1] = Point(0, 0, 0);
    assert true_array[2] = Point(42, 27, 11);
    let res = contains_origin(3, true_array);
    assert res = 1;
    return ();
}
