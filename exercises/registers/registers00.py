def test_ret_42(cairo_run):
    result = cairo_run("ret_42")
    assert result == 42


def test_ret_0_and_1(cairo_run):
    result = cairo_run("ret_0_and_1")
    assert result == [0, 1]
