import pytest


def test_assert_or(cairo_run):
    cairo_run("test_assert_or")


def test_assert_or_ko(cairo_run):
    with pytest.raises(Exception):  # Expecting the function to revert
        cairo_run("test_assert_or_ko")


def test_assert_and(cairo_run):
    cairo_run("test_assert_and")


@pytest.mark.parametrize(
    "test_func", ["test_assert_and_ko1", "test_assert_and_ko2", "test_assert_and_ko3"]
)
def test_assert_and_ko(cairo_run, test_func):
    with pytest.raises(Exception):  # Expecting the function to revert
        cairo_run(test_func)


def test_assert_nor(cairo_run):
    cairo_run("test_assert_nor")


@pytest.mark.parametrize(
    "test_func", ["test_assert_nor_ko1", "test_assert_nor_ko2", "test_assert_nor_ko3"]
)
def test_assert_nor_ko(cairo_run, test_func):
    with pytest.raises(Exception):  # Expecting the function to revert
        cairo_run(test_func)


def test_assert_xor(cairo_run):
    cairo_run("test_assert_xor")


@pytest.mark.parametrize("test_func", ["test_assert_xor_ko", "test_assert_xor_ko2"])
def test_assert_xor_ko(cairo_run, test_func):
    with pytest.raises(Exception):  # Expecting the function to revert
        cairo_run(test_func)
