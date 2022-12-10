import numpy as np
import pytest
from advent_of_code_ocr import convert_array_6
from aocd.models import Puzzle


def parse(data: str) -> list[int]:
    add_ops = []
    for line in data.strip().splitlines():
        match line.split(" "):
            case ["noop"]:
                add_ops.append(0)
            case ["addx", num]:
                # prepend every addx with a noop to simulate two cycles
                add_ops.extend([0, int(num)])
    return add_ops


def part1(add_ops: list[int]) -> int:
    register_values = np.cumsum([1] + add_ops)
    return (register_values[19:220:40] * np.arange(20, 221, 40)).sum()


def part2(add_ops: list[int]) -> str:
    sprite_pos = np.cumsum([1] + add_ops)
    crt_pos = np.arange(len(sprite_pos)) % 40
    sprite_visible = (crt_pos >= sprite_pos - 1) & (crt_pos <= sprite_pos + 1)
    image = sprite_visible[:240].reshape(6, 40)
    return convert_array_6(image, fill_pixel=True, empty_pixel=False)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 10).input_data)


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 13520


def test_example_part1(example_input):
    assert part1(example_input) == 13140


def test_part2(puzzle_input):
    assert part2(puzzle_input) == "PGPHBEAB"


@pytest.fixture()
def example_input():
    return parse(
        """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""
    )
