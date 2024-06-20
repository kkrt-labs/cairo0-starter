import pytest


class TestImplicitSum:
    @pytest.mark.parametrize("a, b, expected", [(3, 5, 8)])
    def test__implicit_sum(self, cairo_run, a, b, expected):
        result = cairo_run("test__sum", a=a, b=b)
        assert result == expected
