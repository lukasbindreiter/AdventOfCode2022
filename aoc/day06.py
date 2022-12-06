import pytest
from aocd.models import Puzzle


def _find(data: str, n: int = 4) -> int:
    for i in range(len(data) - n):
        if len(set(data[i : i + n])) == n:
            return i + n
    return -1


def part1(data: str) -> int:
    return _find(data, 4)


def part2(data: str) -> int:
    return _find(data, 14)


@pytest.fixture()
def puzzle_input() -> str:
    return Puzzle(2022, 6).input_data


@pytest.fixture()
def example_input() -> str:
    return "bvwbjplbgvbhsrlpgdmjqwftvncz"


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 1262


def test_example_part1(example_input):
    assert part1(example_input) == 5


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 3444


def test_example_part2(example_input):
    assert part2(example_input) == 23
