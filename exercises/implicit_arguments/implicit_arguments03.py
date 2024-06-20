import pytest


def string_to_felt(string):
    return int.from_bytes(string.encode("utf-8"), "big")


def felt_to_string(felt):
    length = (felt.bit_length() + 7) // 8
    return felt.to_bytes(length, "big").decode("utf-8")


class TestSecretChange:
    @pytest.mark.parametrize(
        "initial_secret, expected_secret", [("no so secret", "very secret!")]
    )
    def test_secret_change(self, cairo_run, initial_secret, expected_secret):
        secret_felt = string_to_felt(initial_secret)
        result = felt_to_string(cairo_run("test__secret_change", secret=secret_felt))
        assert result == expected_secret
