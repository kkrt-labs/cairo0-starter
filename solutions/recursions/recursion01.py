import pytest


def test_fibonacci(cairo_run):
    cairo_run("test_fibonacci")
