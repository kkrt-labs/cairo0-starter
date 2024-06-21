import pytest

@pytest.mark.parametrize(
    "input_array, expected_output",
    [
        ([1, 2, 3, 4], [1, 4, 9, 16]),
        ([0, 1, 2, 3], [0, 1, 4, 9]),
        ([5, 6, 7], [25, 36, 49]),
        ([], []),
        ([10], [100]),
    ],
)
def test_square(cairo_run, input_array, expected_output):
    result = cairo_run("test__square", array=input_array)
    assert result == expected_output
