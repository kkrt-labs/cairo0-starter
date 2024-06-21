import pytest

def test__hello(cairo_run):
    cairo_run("test_hello")
