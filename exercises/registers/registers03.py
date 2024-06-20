import pytest


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (0, 0, 0),
        (21, 42, 42),
        (42, 21, 42),
    ],
)
def test_max(cairo_run, a, b, expected):
    result = cairo_run("test_max", a=a, b=b)
    assert result == expected


@pytest.mark.parametrize(
    "array",
    [
        [],
        [1],
        [1, 2, 3],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        [10, 20, 30, 40, 50],
        list(range(1, 101)),  # Sum of numbers from 1 to 100
    ],
)
def test_sum_array(cairo_run, array):
    result = cairo_run("test_sum", array=array)
    assert result == sum(array)
