import pytest
import random


def string_to_felt(string):
    return int.from_bytes(string.encode("utf-8"), "big")


class TestBitwise:

    class TestGetNthBit:
        @pytest.mark.parametrize("value, expected", [(0xA8, [0, 0, 0, 1, 0, 1, 0, 1])])
        def test__get_nth_bit(self, cairo_run, value, expected):
            for i in range(8):
                result = cairo_run("get_nth_bit", value=value, n=i)
                assert result == expected[i]

    class TestSetNthBit:
        @pytest.mark.parametrize(
            "value, expected", [(0, [1, 3, 7, 15, 31, 63, 127, 255])]
        )
        def test__set_nth_bit(self, cairo_run, value, expected):
            for i in range(8):
                result = cairo_run("set_nth_bit", value=value, n=i)
                assert result == expected[i]
                value = result

    class TestToggleNthBit:
        @pytest.mark.parametrize(
            "value, n1, n2, n3, expected",
            [
                (int("100000011010111", 2), 14, 3, 5, 2**8 - 1),
            ],
        )
        def test__toggle_nth_bit(self, cairo_run, value, n1, n2, n3, expected):
            res = cairo_run("toggle_nth_bit", value=value, n=n1)
            res = cairo_run("toggle_nth_bit", value=res, n=n2)
            res = cairo_run("toggle_nth_bit", value=res, n=n3)
            assert res == expected

    class TestOpNthBit:
        @pytest.mark.parametrize(
            "v0, v1, v2, n0, n1, n2",
            [
                (
                    random.randint(0, 2**249) + 2**249,
                    random.randint(0, 2**249) + 2**249,
                    random.randint(0, 2**249) + 2**249,
                    random.randint(0, 249),
                    random.randint(0, 249),
                    random.randint(0, 249),
                )
            ],
        )
        def test__op_nth_bit(self, cairo_run, v0, v1, v2, n0, n1, n2):
            if ((v1 >> n1) & 1) == 1:
                v1 = v1 ^ (1 << n1)
            r0 = (v0 >> n0) & 1
            r1 = v1 | (1 << n1)
            r2 = v2 ^ (1 << n2)

            val0 = cairo_run("op_nth_bit", op=string_to_felt("get"), value=v0, n=n0)
            assert r0 == val0
            val1 = cairo_run("op_nth_bit", op=string_to_felt("set"), value=v1, n=n1)
            assert r1 == val1
            val2 = cairo_run("op_nth_bit", op=string_to_felt("toggle"), value=v2, n=n2)
            assert r2 == val2

            with pytest.raises(Exception):
                cairo_run("op_nth_bit", op="rigged", value=v0, n=n1)

        @pytest.mark.parametrize("op, value, n", [("set", 1337, -42)])
        def test__bitwise_bounds_negative_ko(self, cairo_run, op, value, n):
            with pytest.raises(Exception, match="Bad bitwise bounds"):
                cairo_run("op_nth_bit", op=string_to_felt(op), value=value, n=n)

        @pytest.mark.parametrize("op, value, n", [("set", 1337, 251)])
        def test__bitwise_bounds_too_high_ko(self, cairo_run, op, value, n):
            with pytest.raises(Exception, match="Bad bitwise bounds"):
                cairo_run("op_nth_bit", op=string_to_felt(op), value=value, n=n)
