import re
from collections import defaultdict

import pytest
from aocd.models import Puzzle

Stacks = dict[int, list[str]]
Moves = list[tuple[int, int, int]]


def _ints(line: str) -> tuple[int, ...]:
    return tuple(map(int, re.findall(r"\d+", line)))


def parse(data: str) -> tuple[Stacks, Moves]:
    starting_stacks, moves = data.split("\n\n")

    stacks = defaultdict(list)
    for line in starting_stacks.splitlines()[-2::-1]:
        for i, offset in enumerate(range(1, len(line), 4)):
            if line[offset].strip():
                stacks[i + 1].append(line[offset])

    moves = [_ints(move) for move in moves.strip().splitlines()]
    return stacks, moves


def _stack_tops(stacks: Stacks) -> str:
    return "".join(stacks[i][-1] for i in sorted(stacks.keys()))


def part1(stacks: Stacks, moves: Moves) -> str:
    for n, src, dest in moves:
        for _ in range(n):
            stacks[dest].append(stacks[src].pop())

    return _stack_tops(stacks)


def part2(stacks: Stacks, moves: Moves) -> str:
    for n, src, dest in moves:
        stacks[dest].extend(stacks[src][-n:])
        del stacks[src][-n:]

    return _stack_tops(stacks)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 5).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""  # noqa: W291
    )


def test_part1(puzzle_input):
    assert part1(*puzzle_input) == "FWSHSPJWM"


def test_example_part1(example_input):
    assert part1(*example_input) == "CMZ"


def test_part2(puzzle_input):
    assert part2(*puzzle_input) == "PWPWHGFZS"


def test_example_part2(example_input):
    assert part2(*example_input) == "MCD"
