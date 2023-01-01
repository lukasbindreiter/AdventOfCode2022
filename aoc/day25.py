import pytest
from aocd.models import Puzzle

_SNAFU_DIGITS = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
_SNAFU_BASE = len(_SNAFU_DIGITS)

_DECIMAL_TO_SNAFU = {0: "=", 1: "-", 2: "0", 3: "1", 4: "2"}
_SNAFU_OFFSET = 2


def parse(data: str) -> list[str]:
    return data.strip().splitlines()


def snafu_to_decimal(snafu: str) -> int:
    decimal = 0
    for ch in snafu:
        decimal += _SNAFU_DIGITS[ch]
        decimal *= _SNAFU_BASE
    return decimal // _SNAFU_BASE


def decimal_to_snafu(decimal: int) -> str:
    snafu = ""
    while decimal > 0:
        decimal += _SNAFU_OFFSET
        snafu = _DECIMAL_TO_SNAFU[decimal % _SNAFU_BASE] + snafu
        decimal = decimal // _SNAFU_BASE
    return snafu


def part1(snafu_numbers: list[str]) -> str:
    return decimal_to_snafu(sum(map(snafu_to_decimal, snafu_numbers)))


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 25).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
        """.strip()
    )


@pytest.mark.parametrize(
    ("snafu", "expected"), [("1=-0-2", 1747), ("12111", 906), ("2=0=", 198)]
)
def test_snafu_to_decimal(snafu: str, expected: int):
    assert snafu_to_decimal(snafu) == expected


@pytest.mark.parametrize(
    ("decimal", "expected"), [(1747, "1=-0-2"), (906, "12111"), (4890, "2=-1=0")]
)
def test_decimal_to_snafu(decimal: int, expected: str):
    assert decimal_to_snafu(decimal) == expected


def test_part1(puzzle_input):
    assert part1(puzzle_input) == "2=-0=1-0012-=-2=0=01"


def test_example_part1(example_input):
    assert part1(example_input) == "2=-1=0"
