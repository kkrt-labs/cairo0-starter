import pytest


@pytest.mark.parametrize(
    "input_array, expected_output",
    [
        ([1, 2, 3, 4], 1),
        ([1, 2, 69, -11, 0], 0),
        ([10, 9, 8, 7, 6, 5], 0),
        ([1], 1),
        ([1, 1, 1], 1),
        ([], 1),
    ],
)
def test_is_increasing(cairo_run, input_array, expected_output):
    result = cairo_run("test__is_increasing", array=input_array)
    assert result == expected_output


@pytest.mark.parametrize(
    "input_array, expected_output",
    [
        ([1, 2, 3, 4], 0),
        ([1, 2, 69, 11, 0], 0),
        ([10, 9, 8, 7, 6, 5], 1),
        ([1], 1),
        ([1, 1, 1], 1),
        ([], 1),
    ],
)
def test_is_decreasing(cairo_run, input_array, expected_output):
    result = cairo_run("test__is_decreasing", array=input_array)
    assert result == expected_output


@pytest.mark.parametrize(
    "input_array, expected_output",
    [
        ([1, 2, 3, 4, 19, 42], [42, 19, 4, 3, 2, 1]),
        ([31337, 1664, 911, 0], [0, 911, 1664, 31337]),
        ([1], [1]),
        ([], []),
    ],
)
def test_reverse(cairo_run, input_array, expected_output):
    result = cairo_run("test__reverse", array=input_array)
    assert result == expected_output
