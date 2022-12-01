import numpy as np
import pytest
from aocd.models import Puzzle


def parse(data: str) -> list[np.ndarray]:
    elves = data.split("\n\n")
    return [np.fromstring(elf, dtype=int, sep="\n") for elf in elves]


def part1(elf_calories: list[np.ndarray]) -> int:
    sums = [calories.sum() for calories in elf_calories]
    return np.max(sums)


def part2(elf_calories: list[np.ndarray]) -> int:
    sums = np.sort([calories.sum() for calories in elf_calories])
    return sums[-3:].sum()


@pytest.fixture()
def puzzle_input() -> list[np.ndarray]:
    return parse(Puzzle(2022, 1).input_data)


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 67633


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 199628
