import numpy as np
import pytest
from aocd.models import Puzzle
from tqdm import tqdm

MOVES = [0 + 0j, -1 + 0j, 1 + 0j, 0 + 1j, 0 - 1j]


def _coords_of(blizzard_map, symbol):
    indices = np.where(blizzard_map == symbol)
    return set(indices[0] + indices[1] * 1j)


class Blizzards:
    def __init__(self, blizzard_map):
        self.blizzard_map = blizzard_map
        self.height = blizzard_map.shape[0] - 4
        self.width = blizzard_map.shape[1] - 2

        right_moving = _coords_of(blizzard_map, ">")
        left_moving = _coords_of(blizzard_map, "<")
        up_moving = _coords_of(blizzard_map, "^")
        down_moving = _coords_of(blizzard_map, "v")
        self._blizzards = (right_moving, left_moving, up_moving, down_moving)

    @property
    def blizzards(self):
        return set.union(*self._blizzards)

    def is_wall(self, coord):
        return self.blizzard_map[int(coord.real), int(coord.imag)] == "#"

    def step(self):
        right_moving, left_moving, up_moving, down_moving = self._blizzards

        right_moving = {
            b.real + ((b.imag - 1 + 1) % self.width + 1) * 1j for b in right_moving
        }
        left_moving = {
            b.real + ((b.imag - 1 - 1) % self.width + 1) * 1j for b in left_moving
        }
        up_moving = {
            ((b.real - 2 - 1) % self.height + 2) + b.imag * 1j for b in up_moving
        }
        down_moving = {
            ((b.real - 2 + 1) % self.height + 2) + b.imag * 1j for b in down_moving
        }

        self._blizzards = (right_moving, left_moving, up_moving, down_moving)
        return self.blizzards


def parse(data: str) -> list[str]:
    blizzard_map = np.asarray([list(line) for line in data.strip().splitlines()])
    # pad with walls on the top and bottom:
    blizzard_map = np.pad(blizzard_map, ((1, 1), (0, 0)), constant_values="#")
    return Blizzards(blizzard_map)


def _walk(blizzards, start, stop):
    time = 0
    positions = {start}
    with tqdm(total=1000) as pbar:
        while stop not in positions:
            next_positions = set()
            coords = blizzards.step()
            for pos in positions:
                for move in MOVES:
                    next_pos = pos + move
                    if next_pos not in coords and not blizzards.is_wall(next_pos):
                        next_positions.add(next_pos)

            positions = next_positions
            time += 1
            pbar.update(1)

    return time


def part1(blizzards: Blizzards) -> int:
    start = 1 + 1j
    stop = blizzards.height + 2 + blizzards.width * 1j
    return _walk(blizzards, start, stop)


def part2(blizzards: Blizzards) -> int:
    start = 1 + 1j
    stop = blizzards.height + 2 + blizzards.width * 1j
    return (
        _walk(blizzards, start, stop)
        + _walk(blizzards, stop, start)
        + _walk(blizzards, start, stop)
    )


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 24).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
        """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 292


def test_example_part1(example_input):
    assert part1(example_input) == 18


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 816


def test_example_part2(example_input):
    assert part2(example_input) == 54


if __name__ == "__main__":
    print(part2(parse(Puzzle(2022, 24).input_data)))
