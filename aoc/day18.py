import sys
from itertools import combinations

import numpy as np
import pytest
from aocd.models import Puzzle

# simple enough :D
sys.setrecursionlimit(10000)


def parse(data: str) -> list[tuple[int, int, int]]:
    return np.asarray(
        [tuple(map(int, line.split(","))) for line in data.strip().splitlines()]
    )


def shared_side(cube1, cube2) -> bool:
    return sum(abs(cube1[i] - cube2[i]) for i in range(3)) == 1


def part1(cubes: list[tuple[int, int, int]]) -> int:
    shared_sides = sum(
        1 if shared_side(cube1, cube2) else 0 for cube1, cube2 in combinations(cubes, 2)
    )
    return 6 * len(cubes) - 2 * shared_sides


def part2(cubes: list[tuple[int, int, int]]) -> int:
    cubes -= cubes.min(axis=0)  # start with lowest index
    space = np.zeros(shape=(np.max(cubes, axis=0) + 1), dtype=int)
    for x, y, z in cubes:
        space[x, y, z] = 1

    space = np.pad(space, 1, mode="constant")  # make sure the water can flow around
    _flood_fill(space, 0, 0, 0)  # fill all outside cubes with water
    # now treat everything that is not water as the new cube
    cubes = np.asarray(np.where(space[1:-1, 1:-1, 1:-1] < 2)).T
    return part1(cubes)


def _flood_fill(space: np.ndarray, x: int, y: int, z: int):
    if x < 0 or x >= space.shape[0]:
        return
    if y < 0 or y >= space.shape[1]:
        return
    if z < 0 or z >= space.shape[2]:
        return
    if space[x, y, z] != 0:
        return

    space[x, y, z] = 2

    for dx, dy, dz in [
        (-1, 0, 0),
        (1, 0, 0),
        (0, -1, 0),
        (0, 1, 0),
        (0, 0, -1),
        (0, 0, 1),
    ]:
        _flood_fill(space, x + dx, y + dy, z + dz)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 18).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
        """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 3454


def test_example_part1(example_input):
    assert part1(example_input) == 64


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 2014


def test_example_part2(example_input):
    assert part2(example_input) == 58
