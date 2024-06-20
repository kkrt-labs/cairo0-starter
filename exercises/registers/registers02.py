import pytest


def test_crash(cairo_run):
    with pytest.raises(Exception):
        cairo_run("crash")


def test_assert_42(cairo_run):
    cairo_run("test_assert_42", number=42)
    with pytest.raises(Exception):
        cairo_run("test_assert_42", number=21)


def test_assert_pointer_42_initialized(cairo_run):
    cairo_run("test_assert_pointer_42_initialized")


def test_assert_pointer_42_initialized(cairo_run):
    with pytest.raises(Exception):
        cairo_run("test_assert_pointer_42_initialized_ko")


def test_assert_pointer_42_not_initialized_ok(cairo_run):
    cairo_run("test_assert_pointer_42_not_initialized_ok")


def test_assert_pointer_42_not_initialized_revert(cairo_run):
    with pytest.raises(Exception):
        cairo_run("test_assert_pointer_42_not_initialized_revert")


def test_assert_pointer_42_no_set(cairo_run):
    cairo_run("test_assert_pointer_42_no_set")


def test_assert_pointer_42_no_set_ko(cairo_run):
    with pytest.raises(Exception):
        cairo_run("test_assert_pointer_42_no_set_ko")


def test_assert_pointer_42_no_set_crash(cairo_run):
    with pytest.raises(Exception):
        cairo_run("test_assert_pointer_42_no_set_crash")
