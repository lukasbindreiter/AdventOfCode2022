from collections import defaultdict
from itertools import count, cycle
from typing import Optional

import pytest
from aocd.models import Puzzle

DIRECTIONS = [
    (-1 - 1j, -1 + 0j, -1 + 1j),  # north
    (1 - 1j, 1 + 0j, 1 + 1j),  # south
    (-1 - 1j, 0 - 1j, 1 - 1j),  # west
    (-1 + 1j, 0 + 1j, 1 + 1j),  # east
]

NEIGHBOURS_8 = {y + x * 1j for y in range(-1, 2) for x in range(-1, 2)} - {0}


def parse(data: str) -> set[complex]:
    lines = data.strip().splitlines()

    return {
        y + x * 1j
        for y, line in enumerate(lines)
        for x, ch in enumerate(line)
        if ch == "#"
    }


def _simulate(elves: set[complex], n: Optional[int] = None):
    rounds = range(n) if n else count()
    for i, first_direction in zip(rounds, cycle(range(4))):
        elves, no_moves = _round(
            elves, DIRECTIONS[first_direction:] + DIRECTIONS[:first_direction]
        )
        if no_moves:
            return elves, i + 1

    return elves, i + 1


def _round(elves: set[complex], directions: list[tuple[complex, complex, complex]]):
    # First half of the round:
    proposed = defaultdict(list)
    for elf in elves:
        if not any((elf + n) in elves for n in NEIGHBOURS_8):
            continue
        for dirs in directions:
            if not any((elf + d) in elves for d in dirs):
                proposed[elf + dirs[1]].append(elf)
                break

    # Second half:
    moved_elfes = {v[0] for v in proposed.values() if len(v) == 1}
    new_positions = {k for k, v in proposed.items() if len(v) == 1}
    return (elves - moved_elfes) | new_positions, len(moved_elfes) == 0


def _visualize(elves):
    y0, y1, x0, x1 = _bounds(elves)
    out = ""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            out += "#" if (y + x * 1j) in elves else "."
        out += "\n"
    print(out)
    print("----\n\n")


def _bounds(elves: set[complex]):
    ys = [int(elf.real) for elf in elves]
    xs = [int(elf.imag) for elf in elves]
    return min(ys), max(ys), min(xs), max(xs)


def part1(elves: set[complex]) -> int:
    elves, _ = _simulate(elves, 10)
    y0, y1, x0, x1 = _bounds(elves)
    return (y1 - y0 + 1) * (x1 - x0 + 1) - len(elves)


def part2(elves: set[complex]) -> int:
    _, n = _simulate(elves)
    return n


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 23).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
        """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 3766


def test_example_part1(example_input):
    assert part1(example_input) == 110


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 954


def test_example_part2(example_input):
    assert part2(example_input) == 20
