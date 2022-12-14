import pytest
from aocd.models import Puzzle
from numba import complex128, int64, njit
from numba.typed import Dict


def parse(data: str) -> dict:
    # use numba typed dict instead of {} to enable numba jit compilation speed up
    grid = Dict.empty(key_type=complex128, value_type=int64)
    for line in data.strip().splitlines():
        points = [tuple(map(int, p.split(","))) for p in line.split(" -> ")]
        points = [y + x * 1j for x, y in points]
        for start, end in zip(points, points[1:]):
            add_rock_line(grid, start, end)

    return grid


def add_rock_line(grid, start: complex, end: complex):
    diff = end - start
    if diff.real == 0:  # horizontal line
        start_x, stop_x = sorted((start.imag, end.imag))
        for x in range(int(start_x), int(stop_x) + 1):
            grid[start.real + x * 1j] = 1
    elif diff.imag == 0:  # vertical line
        start_y, stop_y = sorted((start.real, end.real))
        for y in range(int(start_y), int(stop_y) + 1):
            grid[y + start.imag * 1j] = 1
    else:
        raise ValueError("points not on the same line")


@njit
def sand_fill(grid: dict, floor: bool = False) -> int:
    n = 0
    while spawn_sand(grid, floor):
        n += 1
    return n


@njit
def spawn_sand(grid: dict, floor: bool = False) -> bool:
    """
    Spawn a new sand element and let it trickle down

    Returns True if the sand stopped, and False if it fell out of bounds or
    stopped if the spawn point is already blocked by sand
    """
    sand = 500j
    if sand in grid:  # stop if we have reached all the way to the top
        return False

    max_y = _max_y(grid)
    while sand.real <= max_y:
        moved = sand_move(grid, sand)
        if moved == sand:  # no move, come to a rest
            grid[sand] = 2
            return True
        sand = moved

    if floor:
        grid[sand] = 2
    return floor  # if we have a floor continue on, otherwise stop (part 1)


@njit
def _max_y(grid: dict) -> int:
    """Maximum y coordinate of a rock in the grid"""
    return int(max([k.real for k, v in grid.items() if v == 1]))


@njit
def sand_move(grid: dict, sand: complex) -> complex:
    """Move sand by one step if possible"""
    for direction in [(1 + 0j), (1 - 1j), (1 + 1j)]:
        if sand + direction not in grid:  # still empty
            return sand + direction
    return sand  # no move possible


def part1(grid: dict) -> int:
    return sand_fill(grid, floor=False)


def part2(grid: dict) -> int:
    return sand_fill(grid, floor=True)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 14).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
        """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 638


def test_example_part1(example_input):
    assert part1(example_input) == 24


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 31722


def test_example_part2(example_input):
    assert part2(example_input) == 93
