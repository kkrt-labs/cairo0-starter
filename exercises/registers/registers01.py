import pytest


def test_assert_is_42_ok(cairo_run):
    cairo_run("assert_is_42", n=42)


def test_assert_is_42_ko(cairo_run):
    with pytest.raises(Exception):  # Expect an exception due to assertion failure
        cairo_run("assert_is_42", n=21)


@pytest.mark.parametrize(
    "a, b, expected_sum",
    [(2, 3, 5), (0, 0, 0), (10, 20, 30)],
)
def test_sum(cairo_run, a, b, expected_sum):
    result = cairo_run("test_sum", a=a, b=b)
    assert result == expected_sum
