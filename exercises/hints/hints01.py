import pytest
import random


class TestModulo:
    @pytest.mark.parametrize(
        "x, n, expected",
        [(random.randint(2, 2**99), random.randint(2, 2**50), None) for _ in range(19)],
    )
    def test__modulo(self, cairo_run, x, n, expected):
        if x < n:
            x, n = n, x
        expected = x % n
        result = cairo_run("modulo", x=x, n=n)
        assert result == expected
