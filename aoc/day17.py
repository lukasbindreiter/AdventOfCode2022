from itertools import cycle
from typing import Iterable

import numpy as np
import pytest
from aocd.models import Puzzle

ROCKS = [
    {0 + 0j, 0 + 1j, 0 + 2j, 0 + 3j},  # ----
    {2 + 1j, 1 + 0j, 1 + 1j, 1 + 2j, 0 + 1j},  # +
    {2 + 2j, 1 + 2j, 0 + 0j, 0 + 1j, 0 + 2j},  # _|
    {3 + 0j, 2 + 0j, 1 + 0j, 0 + 0j},  # |
    {1 + 0j, 1 + 1j, 0 + 0j, 0 + 1j},  # square
]

DIRECTIONS = {
    "<": 0 - 1j,
    ">": 0 + 1j,
}
DOWN = -1 + 0j

SPAWN_POSITION = 3 + 2j
CHAMBER_WIDTH = 7


def parse(data: str) -> list[complex]:
    return list(map(DIRECTIONS.__getitem__, data.strip()))


def iterate_n_times(iterable: Iterable, n: int):
    for val, _ in zip(cycle(iterable), range(n)):
        yield val


def move(rock: set[complex], direction: complex):
    return {c + direction for c in rock}


def _fits_in_chamber(rock: set[complex], chamber_width: int = CHAMBER_WIDTH):
    """
    Check whether the given rock fits in the chamber: True if it fits, false otherwise
    """
    return all(c.imag >= 0 and c.imag < chamber_width for c in rock)


def _collision(rock: set[complex], rocks: set[complex]):
    return any(c.real < 0 for c in rock) or len(rock & rocks) >= 1


def _visualize(rocks: set[complex]):
    """
    Helper function to pretty print the game state to the console
    """
    max_y = int(max(c.real for c in rocks))

    result = ""
    for y in range(max_y + 1, -1, -1):
        result += "|"
        for x in range(CHAMBER_WIDTH):
            result += "#" if (y + x * 1j) in rocks else "."
        result += "|\n"

    result += "+" + ("-" * CHAMBER_WIDTH) + "+"
    print(result)


def _play_tetris(directions, n_rocks: int, debug: bool = False) -> list[int]:
    rocks = set()
    tower_height = 0  # no rock exists yet
    heights = []
    directions = cycle(directions)

    for rock in iterate_n_times(ROCKS, n_rocks):
        rock = move(rock, tower_height + SPAWN_POSITION)
        if debug:
            _visualize(rocks | rock)
            print()

        while True:  # simulate rocks
            # move rock left/right if possible
            rock_moved = move(rock, next(directions))
            if _fits_in_chamber(rock_moved) and not _collision(rock_moved, rocks):
                rock = rock_moved

            rock_down = move(rock, DOWN)
            if _collision(rock_down, rocks):
                break
            rock = rock_down

        # current rock is at its final position, add it to the set of rocks
        rocks = rocks | rock
        tower_height = max([tower_height] + [(c.real + 1) for c in rock])
        heights.append(int(tower_height))

    return heights


def part1(directions: list[complex]) -> int:
    return _play_tetris(directions, 2022)[-1]


def part2(directions: list[complex]) -> int:
    # we need to find a repeating pattern in the tower heights
    heights = _play_tetris(directions, 20000)
    # lets look at the differences in height after each block
    diffs = np.diff(heights)

    # and try to find a pattern in there:
    # min and max length found after some experimentation on the example and real data
    pattern_start, pattern_length = find_repeating_pattern(diffs, 10, 3000)
    pattern_height = heights[pattern_start + pattern_length] - heights[pattern_start]

    # now use this pattern to just calculate the height at the final position
    total = 1000000000000

    # use the real height at the moment just before the repeating pattern starts:
    remaining_blocks = total - (pattern_start + 1)
    tower_height = heights[pattern_start]

    # simulate repeating the pattern many many many times:
    tower_height += (remaining_blocks // pattern_length) * pattern_height

    # if few blocks may be remaining in the end, add those as well:
    remaining_blocks = remaining_blocks % pattern_length
    tower_height += heights[pattern_start + remaining_blocks] - heights[pattern_start]

    return tower_height


def find_repeating_pattern(
    values: list[int], min_length: int, max_length: int
) -> int | int:
    """
    Find a sequence in the given list with a length between min_length and max_length
    which repeats at least 3 times:
    """
    for i in range(len(values) - 3 * max_length):
        for length in range(min_length, max_length):
            if all(
                values[i : i + length] == values[i + length : i + 2 * length]
            ) and all(
                values[i + length : i + 2 * length]
                == values[i + 2 * length : i + 3 * length]
            ):
                return i, length

    return None


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 17).input_data)


@pytest.fixture()
def example_input():
    return parse(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>")


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 3239


def test_example_part1(example_input):
    assert part1(example_input) == 3068


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 1594842406882


def test_example_part2(example_input):
    assert part2(example_input) == 1514285714288
