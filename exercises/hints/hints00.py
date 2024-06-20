import pytest


class TestHints00:
    def test__basic_hint(self, cairo_run):
        expected = 41
        result = cairo_run("basic_hint")
        assert expected == result - 1
