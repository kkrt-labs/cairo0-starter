
import pytest

def test__say_hello(cairo_run):
    cairo_run("test_say_hello")
