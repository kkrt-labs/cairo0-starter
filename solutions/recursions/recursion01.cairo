// Fibonacci numbers are defined by the following recurrence:
// F(0) = 0
// F(1) = 1
// F(n) = F(n-1) + F(n-2)

// I AM NOT DONE

// TODO: write a recursive implementation of fibonacci numbers that returns the nth fibonacci number

func fibonacci(n: felt) -> felt {
    alloc_locals;
    if (n == 0) {
        return 0;
    }
    if (n == 1) {
        return 1;
    }
    let n_1 = fibonacci(n - 1);
    let n_2 = fibonacci(n - 2);
    return n_1 + n_2;
}

// Do not change the test
func test_fibonacci{syscall_ptr: felt*}() {
    let n = fibonacci(0);
    assert n = 0;
    let n = fibonacci(1);
    assert n = 1;
    let n = fibonacci(7);
    assert n = 13;
    let n = fibonacci(10);
    assert n = 55;
    return ();
}
