from dataclasses import dataclass
from typing import Callable

import numpy as np
import pytest
from aocd.models import Puzzle
from parse import search

_MONKEY_INPUT_FORMAT = """
Monkey {monkey_id:d}:
  Starting items: {items}
  Operation: new = old {op} {operand}
  Test: divisible by {test:d}
    If true: throw to monkey {next_true:d}
    If false: throw to monkey {next_false:d}
""".strip()


@dataclass
class Monkey:
    monkey_id: int
    items: list[int]
    operation: Callable[[int], int]
    test: int
    next_monkey: dict[bool, int]
    n_inspections: int

    def __repr__(self) -> str:
        return f"Monkey {self.monkey_id}: {', '.join(map(str, self.items))}"

    @classmethod
    def from_str(cls, monkey_data: str):
        monkey = search(_MONKEY_INPUT_FORMAT, monkey_data).named

        operand, mul = monkey["operand"], monkey["op"] == "*"
        try:
            operand = int(operand)
            op = (lambda x: x * operand) if mul else (lambda x: x + operand)
        except ValueError:
            op = (lambda x: x * x) if mul else (lambda x: x + x)

        return cls(
            monkey["monkey_id"],
            list(map(int, monkey["items"].split(", "))),
            op,
            monkey["test"],
            {True: monkey["next_true"], False: monkey["next_false"]},
            0,
        )


class MonkeyGame:
    def __init__(self, monkeys: list[Monkey], worry_downscale: Callable[[int], int]):
        self.monkeys = monkeys
        self.worry_downscale = worry_downscale

    def __repr__(self) -> str:
        return "\n".join(map(str, self.monkeys))

    def single_round(self):
        for monkey in self.monkeys:
            for item in monkey.items:
                worry = monkey.operation(item)
                worry = self.worry_downscale(worry)
                next_monkey = monkey.next_monkey[(worry % monkey.test) == 0]
                self.monkeys[next_monkey].items.append(worry)
            monkey.n_inspections += len(monkey.items)
            monkey.items = []

    @property
    def monkey_business(self):
        inspections = sorted(m.n_inspections for m in self.monkeys)
        return inspections[-1] * inspections[-2]


def parse(data: str) -> list[Monkey]:
    return [Monkey.from_str(s) for s in data.split("\n\n")]


def part1(monkeys: list[Monkey]) -> int:
    game = MonkeyGame(monkeys, lambda worry: worry // 3)
    for _ in range(20):
        game.single_round()

    return game.monkey_business


def part2(monkeys: list[Monkey]) -> int:
    common_multiple = np.prod([monkey.test for monkey in monkeys])
    game = MonkeyGame(monkeys, lambda worry: worry % common_multiple)

    for _ in range(10000):
        game.single_round()

    return game.monkey_business


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 11).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 112221


def test_example_part1(example_input):
    assert part1(example_input) == 10605


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 25272176808


def test_example_part2(example_input):
    assert part2(example_input) == 2713310158
