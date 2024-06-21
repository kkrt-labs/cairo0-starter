import pytest


class TestFelts:
    def test_felt(self, cairo_run):
        cairo_run("test__felt")
