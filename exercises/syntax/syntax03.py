import pytest


@pytest.mark.parametrize("a, b", [(2, 3), (0, 0), (10, 20)])
def test__sum(cairo_run, a, b):
    result = cairo_run("test_sum", a=a, b=b)
    assert result == a + b
