import numpy as np
import pytest
from aocd.models import Puzzle

DECRYPTION_KEY = 811589153


def parse(data: str) -> list[str]:
    return np.asarray(list(map(int, data.strip().splitlines())))


def _find(array: np.ndarray, value: int):
    return np.where(array == value)[0].item()


def _mix(values: np.ndarray, n: int = 1):
    indices = np.arange(len(values))
    for _ in range(n):
        for i in range(len(values)):
            curr_index = _find(indices, i)
            new_index = (curr_index + values[i]) % (len(values) - 1)

            save = indices[curr_index]
            if curr_index <= new_index:  # move to the right
                indices[curr_index:new_index] = indices[curr_index + 1 : new_index + 1]
            else:  # move to the left
                indices[new_index + 1 : curr_index + 1] = indices[new_index:curr_index]
            indices[new_index] = save

    return values[indices]


def part1(values: np.ndarray, n: int = 1) -> int:
    values = _mix(values, n)
    positions = (np.asarray([1000, 2000, 3000]) + _find(values, 0)) % len(values)
    return values[positions].sum()


def part2(values: np.ndarray) -> int:
    values *= DECRYPTION_KEY
    return part1(values, n=10)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 20).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
1
2
-3
3
-2
0
4
        """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 5962


def test_example_part1(example_input):
    assert part1(example_input) == 3


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 9862431387256


def test_example_part2(example_input):
    assert part2(example_input) == 1623178306
