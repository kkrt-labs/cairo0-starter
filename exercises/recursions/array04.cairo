%lang starknet

from starkware.cairo.common.math_cmp import is_not_zero

struct Point {
    x : felt,
    y : felt,
    z : felt,
}

func contains_origin{range_check_ptr : felt}(len_points : felt, points : Point*) -> felt {
    // FILL ME
    if (len_points == 0) {
        return 0;
    }

    let point = points[0];
    tempvar not_x = is_not_zero(point.x);
    tempvar not_y = is_not_zero(point.y);
    tempvar not_z = is_not_zero(point.z);

    let not_origin = not_x + not_y + not_z;
    if (not_origin == 0) {
        return 1;
    }
    return contains_origin(len_points - 1, points + Point.SIZE);
}

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
