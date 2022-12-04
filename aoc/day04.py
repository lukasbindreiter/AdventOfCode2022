import re

import pytest
from aocd.models import Puzzle


def parse(data: str) -> list[tuple[range, range]]:
    ranges = []
    for line in data.strip().splitlines():
        a0, a1, b0, b1 = map(int, re.findall(r"\d+", line))
        ranges.append((set(range(a0, a1 + 1)), set(range(b0, b1 + 1))))
    return ranges


def _part_x(ranges: list[tuple[range, range]], comparison_operator):
    return sum(
        1 if (comparison_operator(a, b) or comparison_operator(b, a)) else 0
        for a, b in ranges
    )


def part1(ranges: list[tuple[range, range]]) -> int:
    return _part_x(ranges, set.issubset)


def part2(ranges: list[tuple[range, range]]) -> int:
    return _part_x(ranges, set.intersection)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 4).input_data)


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 496


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 847
