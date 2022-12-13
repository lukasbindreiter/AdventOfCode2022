from functools import cmp_to_key

import pytest
from aocd.models import Puzzle


def parse(data: str):
    packets = data.strip().splitlines()
    # ¯\_(ツ)_/¯
    return [eval(packet) for packet in packets if packet]


def compare(left: list | int, right: list | int):
    """
    Compare left and right, returning:
    number < 0 if left is smaller
    0 if they are equal
    number > 0 if right is smaller
    """
    match (left, right):
        case int(left), int(right):
            return left - right
        case int(left), right:
            return compare([left], right)
        case left, int(right):
            return compare(left, [right])
        case left, right:
            for left_val, right_val in zip(left, right):
                comparison = compare(left_val, right_val)
                if comparison != 0:
                    return comparison
            # list length as potential tiebreaker
            return len(left) - len(right)
    return 0


def part1(packets) -> int:
    sum_in_order = 0
    for i, (left, right) in enumerate(zip(packets[::2], packets[1::2]), start=1):
        if compare(left, right) < 0:
            sum_in_order += i

    return sum_in_order


def part2(packets) -> int:
    divider1 = [[2]]
    divider2 = [[6]]
    packets = packets + [divider1, divider2]
    packets.sort(key=cmp_to_key(compare))
    return (packets.index(divider1) + 1) * (packets.index(divider2) + 1)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 13).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
        """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 5013


def test_example_part1(example_input):
    assert part1(example_input) == 13


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 25038


def test_example_part2(example_input):
    assert part2(example_input) == 140
