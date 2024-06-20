import pytest

def test_poly_high_level(cairo_run):
    @pytest.mark.parametrize("x, expected", [
        (0, 67),
        (1, 136),
        (2, 251),
        (3, 436),
        (10, 3267),
        (-1, 0),  # x^3 + 23x^2 + 45x + 67 = -1 + 23 - 45 + 67 = 44, which is 0 in the field
        (1000, 1023067000),  # Large number
    ])
    def _test(x, expected):
        result = cairo_run("test_poly_high_level", x=x)
        assert result == expected, f"For x={x}, expected {expected} but got {result}"

    _test()

def test_poly_low_level(cairo_run):
    @pytest.mark.parametrize("x, expected", [
        (0, 67),
        (1, 136),
        (2, 251),
        (3, 436),
        (10, 3267),
        (-1, 0),  # x^3 + 23x^2 + 45x + 67 = -1 + 23 - 45 + 67 = 44, which is 0 in the field
        (1000, 1023067000),  # Large number
    ])
    def _test(x, expected):
        result = cairo_run("test_poly_low_level", x=x)
        assert result == expected, f"For x={x}, expected {expected} but got {result}"

    _test()

@pytest.mark.parametrize("x", [0, 1, 2, 3, 10, -1, 1000])
def test_poly_equality(cairo_run, x):
    high_level_result = cairo_run("test_poly_high_level", x=x)
    low_level_result = cairo_run("test_poly_low_level", x=x)
    assert high_level_result == low_level_result, f"For x={x}, high-level and low-level results differ"

def calculate_expected(x):
    return x**3 + 23*x**2 + 45*x + 67

@pytest.mark.parametrize("x", range(-10, 11))  # Test for x from -10 to 10
def test_poly_correctness(cairo_run, x):
    high_level_result = cairo_run("test_poly_high_level", x=x)
    expected = calculate_expected(x) % 2**251  # Apply modulo to match Cairo's field arithmetic
    assert high_level_result == expected, f"For x={x}, expected {expected} but got {high_level_result}"
