import pytest
from aocd.models import Puzzle


def parse(data: str) -> list[tuple[str, str]]:
    return [line.split() for line in data.strip().splitlines()]


def _char_to_num(ch: str, offset: str) -> int:
    """
    Convert the given char to a numeric value, starting at the given offset char with 1

    >>> _char_to_num("Y", "X")
    2
    """
    return ord(ch) - ord(offset) + 1


def _calc_round_score(opponent_move: int, own_move: int) -> int:
    """
    Calculate the score for one round of rock paper scissors

    outcome:
        0 => draw => 3 points  ((0 + 1) % 3) * 3 => 3
        1 => win => 6 points  ((1 + 1) % 3) * 3 => 6
        2 => lose => 0 points  ((2 + 1) % 3) * 3 => 0
    """
    outcome = (own_move - opponent_move) % 3
    return (outcome + 1) % 3 * 3 + own_move


def part1(strategy: list[tuple[str, str]]) -> int:
    games = [(_char_to_num(ch1, "A"), _char_to_num(ch2, "X")) for ch1, ch2 in strategy]
    return sum((_calc_round_score(opponent, own)) for opponent, own in games)


def _find_round_move_for_outcome(opponent_move: int, desired_outcome: int):
    # map outcomes like above:
    # 0 => draw, 1 => win, 2 => lose
    desired_outcome = (desired_outcome + 1) % 3
    # we can calculate the outcome like this (see above)
    # outcome = (own_move - opponent_move) % 3
    # so let's just solve that for (own_move) instead:
    return (desired_outcome + opponent_move) % 3 or 3  # (instead of 0 we want 3)


def part2(strategy: list[tuple[str, str]]) -> int:
    games = [(_char_to_num(ch1, "A"), _char_to_num(ch2, "X")) for ch1, ch2 in strategy]
    games = [
        (opponent_move, _find_round_move_for_outcome(opponent_move, desired_outcome))
        for opponent_move, desired_outcome in games
    ]
    return sum((_calc_round_score(opponent, own)) for opponent, own in games)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 2).input_data)


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 9759


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 12429
