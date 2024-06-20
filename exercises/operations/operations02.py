import pytest


class TestSolve:
    def test_solve(self, cairo_run, a):
        cairo_run("test__solve")
