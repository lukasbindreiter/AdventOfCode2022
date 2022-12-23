import re

import numpy as np
import pytest
from aocd.models import Puzzle

RIGHT = 0 + 1j
DOWN = 1 + 0j
LEFT = 0 - 1j
UP = -1 + 0j
FACINGS = [RIGHT, DOWN, LEFT, UP]
TURNS = {"L": 1j, "R": -1j}


def parse(data: str) -> tuple[np.ndarray, list[tuple[int, str]]]:
    board, path = data.split("\n\n")

    lines = board.splitlines()
    arr = np.zeros(shape=(len(lines), len(lines[0])), dtype=int)
    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            arr[y, x] = {".": 0, "#": 1}.get(ch, -1)

    path = [(int(seg[:-1]), seg[-1]) for seg in re.findall(r"\d+[LR]", path + "L")]

    return arr, path


class WrappedBoard2D:
    def __init__(self, board: np.ndarray) -> None:
        self.board = board
        self.pos = 0 + 50j  # hardcoded for real input
        self.facing = RIGHT

    def walk(self, path: list[tuple[int, str]]):
        for n, turn in path:
            for _ in range(n):
                self.step()
            self.turn(turn)

        self.turn("R")  # reverse the very last left turn we appended

    def turn(self, direction: str):
        self.facing = self.facing * TURNS[direction]

    def step(self):
        next_pos, next_facing = self._wrap(self.pos, self.facing)
        if self.is_empty(next_pos):
            self.pos = next_pos
            self.facing = next_facing

    def _wrap(self, pos, facing):
        pos = pos + facing
        if facing in (LEFT, RIGHT):
            return self._wrap_left_right(pos, facing)
        return self._wrap_up_down(pos, facing)

    def _wrap_left_right(self, pos, facing):
        if 0 <= pos.real < 50:
            return pos.real + ((int(pos.imag - 50) % 100) + 50) * 1j, facing
        if pos.real < 100:
            return pos.real + ((int(pos.imag - 50) % 50) + 50) * 1j, facing
        if pos.real < 150:
            return pos.real + (int(pos.imag) % 100) * 1j, facing

        return pos.real + (int(pos.imag) % 50) * 1j, facing

    def _wrap_up_down(self, pos, facing):
        if 0 <= pos.imag < 50:
            return ((int(pos.real - 100) % 100) + 100) + pos.imag * 1j, facing
        if pos.imag < 100:
            return (int(pos.real) % 150) + pos.imag * 1j, facing

        return (int(pos.real) % 50) + pos.imag * 1j, facing

    def is_empty(self, pos: complex):
        try:
            val = self.board[int(pos.real), int(pos.imag)]
            assert val >= 0  # never end up in no mans land
            return val == 0
        except IndexError:
            print(f"At: {pos=}")
            raise

    def password(self):
        return int(
            1000 * (self.pos.real + 1)
            + 4 * (self.pos.imag + 1)
            + FACINGS.index(self.facing)
        )


def part1(arr: np.ndarray, path: list[tuple[int, str]]) -> int:
    board = WrappedBoard2D(arr)
    board.walk(path)
    return board.password()


# the cube layout
"""
    |---|---|
    | A | B |
    |---|---|
    | C |
|---|---|
| D | E |
|---|---|
| F |
|---|
"""


class WrappedBoard3D(WrappedBoard2D):
    def _wrap(self, pos, facing):
        pos = pos + facing
        if facing == UP:
            y, x, facing = self._wrap_up(pos.real, pos.imag, facing)
        elif facing == DOWN:
            y, x, facing = self._wrap_down(pos.real, pos.imag, facing)
        elif facing == RIGHT:
            y, x, facing = self._wrap_right(pos.real, pos.imag, facing)
        elif facing == LEFT:
            y, x, facing = self._wrap_left(pos.real, pos.imag, facing)

        return y + x * 1j, facing

    def _wrap_up(self, y, x, facing):
        """Wrap along the 3 up facing edges (A, B, D)"""
        if y == -1 and 50 <= x < 100:  # moved up from A -> F
            return (x + 100), 0, RIGHT
        if y == -1 and 100 <= x < 150:  # moved up from B -> F
            return 199, (x - 100), UP
        if y == 99 and 0 <= x < 50:  # moved from D -> C
            return (x + 50), 50, RIGHT
        return y, x, facing

    def _wrap_down(self, y, x, facing):
        """Wrap along the 3 down facing edges (B, E, F)"""
        if y == 50 and 100 <= x < 150:  # moved down from B -> C
            return x - 50, 99, LEFT
        if y == 150 and 50 <= x < 100:  # moved down from E -> F
            return x + 100, 49, LEFT
        if y == 200 and 0 <= x < 50:  # moved down from F -> B
            return 0, x + 100, DOWN
        return y, x, facing

    def _wrap_right(self, y, x, facing):
        """Wrap along the 4 right facing edges (B, C, E, F)"""
        if x == 150 and 0 <= y < 50:  # moved right from B -> E
            return (49 - y) + 100, 99, LEFT
        if x == 100 and 50 <= y < 100:  # moved right from C -> B
            return 49, y + 50, UP
        if x == 100 and 100 <= y < 150:  # moved right from E -> B
            return (149 - y), 149, LEFT
        if x == 50 and 150 <= y < 200:  # moved right from F -> E
            return 149, y - 100, UP
        return y, x, facing

    def _wrap_left(self, y, x, facing):
        """Wrap along the 4 left facing edges (A, C, D, F)"""
        if x == 49 and 0 <= y < 50:  # moved left from A -> D
            return (49 - y) + 100, 0, RIGHT
        if x == 49 and 50 <= y < 100:  # moved left from C -> D
            return 100, y - 50, DOWN
        if x == -1 and 100 <= y < 150:  # moved left from D -> A
            return (149 - y), 50, RIGHT
        if x == -1 and 150 <= y < 200:  # moved left from F -> A
            return 0, y - 100, DOWN
        return y, x, facing


def part2(arr: np.ndarray, path: list[tuple[int, str]]) -> int:
    board = WrappedBoard3D(arr)
    board.walk(path)
    return board.password()


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 22).input_data)


def test_part1(puzzle_input):
    assert part1(*puzzle_input) == 93226


def test_part2(puzzle_input):
    assert part2(*puzzle_input) == 37415
