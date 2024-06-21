import pytest


def test__currency_sum(cairo_run):
    cairo_run("test_currency_sum")
