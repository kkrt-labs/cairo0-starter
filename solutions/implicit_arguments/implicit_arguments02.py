import pytest

class TestImplicitArguments:
    @pytest.mark.parametrize(
        "a, b",
        [
            (3, 5)
        ]
    )
    def test__sum(self, cairo_run, a, b):
        result = cairo_run("test__sum", a=a, b=b)
        assert result == 14
