from functools import partial
from typing import Callable

import pytest
from aocd.models import Puzzle


def parse(data: str) -> dict[str, int | tuple[str, str, str]]:
    monkeys = {}
    for line in data.strip().splitlines():
        name, number = line.split(": ")
        try:
            monkeys[name] = int(number)
        except ValueError:
            monkeys[name] = tuple(number.split(" "))
    return monkeys


def _expr(monkey_funcs, left, right, op):
    return int(op(monkey_funcs[left](), monkey_funcs[right]()))


def _constant(val):
    return val


OPERATORS = {"+": int.__add__, "-": int.__sub__, "*": int.__mul__, "/": int.__truediv__}


def _construct_top_down_solving_functions(
    equations: dict[str, int | tuple[str, str, str]]
) -> dict[str, Callable[[], int]]:
    top_down = {}
    for result, expr in equations.items():
        match expr:
            case int(val):
                top_down[result] = partial(_constant, val=val)
            case left, op, right:
                top_down[result] = partial(_expr, top_down, left, right, OPERATORS[op])
    return top_down


def part1(monkeys: dict[str, int | tuple[str, str, str]]) -> int:
    monkey_funcs = _construct_top_down_solving_functions(monkeys)
    return monkey_funcs["root"]()


def part2(equations: dict[str, int | tuple[str, str, str]]) -> int:
    equations.pop("humn")  # so it will raise a key error when looking for it
    monkey_funcs = _construct_top_down_solving_functions(equations)
    return _solve(equations, monkey_funcs, "root", 0)


def _solve(monkeys: dict, functions: dict, name: str, value: int = None):
    if name == "humn":
        return value

    left, op, right = monkeys.pop(name)
    if name == "root":
        op = "="

    try:
        left_val = functions[left]()
    except KeyError:  # humn is in the left branch, we need to solve for that
        right_val = functions[right]()
        match op:
            # left == right
            case "=":
                return _solve(monkeys, functions, left, right_val)
            # value = left + right => left = value - right
            case "+":
                return _solve(monkeys, functions, left, value - right_val)
            # value = left - right => left = value + right
            case "-":
                return _solve(monkeys, functions, left, value + right_val)
            # value = left * right => left = value / right
            case "*":
                return _solve(monkeys, functions, left, value // right_val)
            # value = left / right => left = value * right
            case "/":
                return _solve(monkeys, functions, left, value * right_val)

    # if we didn't return above then humn is in the right branch -> solve for that
    match op:
        # left == right
        case "=":
            return _solve(monkeys, functions, right, left_val)
        # value = left + right => right = value - left
        case "+":
            return _solve(monkeys, functions, right, value - left_val)
        # value = left - right => right = left - value
        case "-":
            return _solve(monkeys, functions, right, left_val - value)
        # value = left * right => right = value / left
        case "*":
            return _solve(monkeys, functions, right, value // left_val)
        # value = left / right => right = left / value
        case "/":
            return _solve(monkeys, functions, right, left_val // value)

    return value


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 21).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
        """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 75147370123646


def test_example_part1(example_input):
    assert part1(example_input) == 152


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 3423279932937


def test_example_part2(example_input):
    assert part2(example_input) == 301
