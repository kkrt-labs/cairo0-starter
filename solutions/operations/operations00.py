import pytest


class TestPoly:
    @pytest.mark.parametrize("x, expected", [(1, 0), (3, 10)])
    def test_poly(self, cairo_run, x, expected):
        result = cairo_run("poly", x=x)
        assert result == expected
