import pytest


def test_ternary_conditional_operator(cairo_run):
    cairo_run("test_ternary_conditional_operator")


def test_ternary_conditional_operator_ko(cairo_run):
    with pytest.raises(Exception):
        cairo_run("test_ternary_conditional_operator_ko")
