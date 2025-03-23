// As with many other languages, you can describe object structures with the struct keyword.

// I AM NOT DONE

// TODO: declare the Currency struct to make the test pass

// Do not change the test
func test_currency_sum() {
    alloc_locals;
    local euro: Currency = Currency('Euro', 2);
    assert euro.name = 'Euro';
    return ();
}
