import pytest


@pytest.mark.parametrize(
    "needle, haystack, expected",
    [
        (3, [1, 2, 3, 4], 1),
        (5, [1, 2], 0),
        (1, [1, 2, 3, 4], 1),
        (4, [1, 2, 3, 4], 1),
        (0, [1, 2, 3, 4], 0),
        (6, [], 0),
    ],
)
def test_contains(cairo_run, needle, haystack, expected):
    result = cairo_run("test__contains", needle=needle, haystack=haystack)
    assert result == expected
