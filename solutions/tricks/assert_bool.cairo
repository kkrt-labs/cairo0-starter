%lang starknet

// Boolean assertions, such as "x OR y" for boolean felts, can also be implemented without conditionals.

// I AM NOT DONE

// TODO Implement the following boolean asserts without "if"

func assert_or(x, y) {
    assert 0 = (x - 1) * (y - 1);
    return ();
}

func assert_and(x, y) {
    assert 2 = x + y;
    // assert 1 = x * y // works too
    return ();
}

func assert_nor(x, y) {
    assert 0 = x + y;
    return ();
}

func assert_xor(x, y) {
    assert 1 = x + y;
    return ();
}

// Do not modify the tests
func test_assert_or() {
    assert_or(0, 1);
    assert_or(1, 0);
    assert_or(1, 1);
    return ();
}

func test_assert_or_ko() {
    assert_or(0, 0);
    return ();
}

func test_assert_and() {
    assert_and(1, 1);
    return ();
}

func test_assert_and_ko1() {
    assert_and(0, 0);
    return ();
}

func test_assert_and_ko2() {
    assert_and(0, 1);
    return ();
}

func test_assert_and_ko3() {
    assert_and(1, 0);
    return ();
}

func test_assert_nor() {
    assert_nor(0, 0);
    return ();
}

func test_assert_nor_ko1() {
    assert_nor(0, 1);
    return ();
}

func test_assert_nor_ko2() {
    assert_nor(1, 0);
    return ();
}

func test_assert_nor_ko3() {
    assert_nor(1, 1);
    return ();
}

func test_assert_xor() {
    assert_xor(0, 1);
    assert_xor(1, 0);
    return ();
}

func test_assert_xor_ko() {
    assert_xor(0, 0);
    return ();
}

func test_assert_xor_ko2() {
    assert_xor(1, 1);
    return ();
}
