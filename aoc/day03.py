import pytest
from aocd.models import Puzzle


def parse(data: str) -> list[str]:
    return data.strip().splitlines()


def _half_half(line: str):
    n = len(line) // 2
    return line[:n], line[n:]


def _to_priority(char: str):
    if char.isupper():
        return ord(char) - ord("A") + 27
    return ord(char) - ord("a") + 1


def part1(rucksacks: list[str]) -> int:
    contents = [_half_half(line) for line in rucksacks]
    items = []
    for compartment1, compartment2 in contents:
        (common,) = set(compartment1) & set(compartment2)
        items.append(common)
    return sum(map(_to_priority, items))


def part2(rucksacks: list[str]) -> int:
    items = []
    for items1, items2, items3 in zip(rucksacks[::3], rucksacks[1::3], rucksacks[2::3]):
        (common,) = set(items1) & set(items2) & set(items3)
        items.append(common)
    return sum(map(_to_priority, items))


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 3).input_data)


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 7824


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 2798
