import pytest


@pytest.mark.parametrize(
    "x",
    [0, 1, 2, 3, 10, -1, 1000],
)
def test_poly_high_level(cairo_run, x):
    result = cairo_run("test_poly_high_level", x=x)
    expected = x**3 + 23 * x**2 + 45 * x + 67
    assert result == expected


@pytest.mark.parametrize(
    "x",
    [
        0,
        1,
        2,
        3,
        10,
        -1,
        1000,
    ],
)
def test_poly_low_level(cairo_run, x):
    result = cairo_run("test_poly_low_level", x=x)
    expected = x**3 + 23 * x**2 + 45 * x + 67
    assert result == expected
