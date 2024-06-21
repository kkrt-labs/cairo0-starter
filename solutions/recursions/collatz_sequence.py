import pytest


def test__collatz_sequence(cairo_run):
    cairo_run("test_collatz")
