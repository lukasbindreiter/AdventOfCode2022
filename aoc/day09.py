from itertools import chain

import numpy as np
import pytest
from aocd.models import Puzzle
from numba import complex128, int64, njit

# use complex numbers to store 2d coordinates
DIRECTIONS = {"U": -1 + 0j, "R": 0 + 1j, "D": 1 + 0j, "L": 0 - 1j}


def parse(data: str) -> list[str]:
    """
    Generate a list of single character moves from a given input

    R 3
    U 2
    D 2

    > ["R", "R", "R", "U", "U", "D", "D"]

    and convert them directly to their direction values

    > [1j, 1j, 1j, -1, -1, 1, 1]
    """
    moves = [line.split(" ") for line in data.splitlines()]
    moves = chain.from_iterable([direction] * int(times) for direction, times in moves)
    moves = list(moves)
    return np.fromiter(map(DIRECTIONS.__getitem__, moves), complex, len(moves))


@njit(complex128(complex128))
def _direction_vec(val: complex) -> complex:
    """
    Clip the given value to a maximum the knot can move (1 vertical and 1 horizontal)
    """
    return np.sign(val.real) + np.sign(val.imag) * 1j


@njit(int64(complex128[:]))
def part1(moves: np.ndarray) -> int:
    head, tail = 0, 0
    tail_positions = {tail}

    for move in moves:
        head += move
        distance = head - tail
        tail_move = _direction_vec(distance) if np.abs(distance) >= 2 else 0
        tail += tail_move
        tail_positions.add(tail)

    return len(tail_positions)


@njit(int64(complex128[:]))
def part2(moves: np.ndarray) -> int:
    knots = np.zeros(10, dtype=np.complex128)
    tail_positions = {knots[-1]}

    for move in moves:
        knots[0] += move

        for i in range(1, len(knots)):
            head, tail = knots[i - 1], knots[i]
            distance = head - tail
            tail_move = _direction_vec(distance) if np.abs(distance) >= 2 else 0
            knots[i] += tail_move

        tail_positions.add(knots[-1])

    return len(tail_positions)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 9).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
    """.strip()
    )


@pytest.fixture()
def larger_example_input():
    return parse(
        """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
    """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 6023


def test_example_part1(example_input):
    assert part1(example_input) == 13


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 2533


def test_example_part2(example_input):
    assert part2(example_input) == 1


def test_larger_example_part2(larger_example_input):
    assert part2(larger_example_input) == 36
