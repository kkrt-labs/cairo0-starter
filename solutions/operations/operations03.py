import pytest


class TestSolve:
    def test_solve(self, cairo_run):
        cairo_run("test_solve")
