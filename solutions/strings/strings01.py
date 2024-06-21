import pytest

def test__decode_string(cairo_run):
    cairo_run("test_decode_string")
