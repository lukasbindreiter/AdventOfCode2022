import numpy as np
import pytest
from aocd.models import Puzzle


def parse(data: str) -> np.ndarray:
    return np.asarray([[int(v) for v in line] for line in data.strip().split()])


def _visible_from_top(forest: np.ndarray) -> np.ndarray:
    """
    Return a boolean array indicating which trees in the given forest are visible
    if viewed from the top
    """
    # add row of -1 values to the top, so that the edges will always be visible
    # since they are (larger than the -1 in front)
    padded = np.pad(forest, ((1, 0), (0, 0)), constant_values=-1)
    return forest > np.maximum.accumulate(padded)[:-1, :]


def part1(forest: np.ndarray) -> int:
    """
    Count how many trees are visible from any of the four directions
    """
    visible = np.zeros_like(forest)
    # Reuse the visible from top function for all directions by flipping and transposing
    # the array accordingly:
    visible |= _visible_from_top(forest)  # from top
    visible |= _visible_from_top(forest.T).T  # from left
    visible |= _visible_from_top(forest[::-1, :])[::-1, :]  # from bottom
    visible |= _visible_from_top(forest[:, ::-1].T).T[:, ::-1]  # from right

    return visible.sum()


def _scenic_score(forest: np.ndarray, y: int, x: int) -> int:
    """
    Calculate the scenic score for a given position in the forest
    """
    own_height = forest[y, x]
    up = forest[:y, x][::-1]  # 1d array of trees when looking up
    left = forest[y, :x][::-1]  # 1d array of trees when looking left
    right = forest[y, x + 1 :]  # 1d array of trees when looking right
    down = forest[y + 1 :, x]  # 1d array of trees when looking down

    def _view_distance(trees) -> int:
        maxs = np.maximum.accumulate(trees)
        return (own_height > maxs).sum() + (1 if maxs[-1] >= own_height else 0)

    return (
        _view_distance(up)
        * _view_distance(left)
        * _view_distance(right)
        * _view_distance(down)
    )


def part2(forest: np.ndarray) -> int:
    """
    Find the maximum scenic score in a forest
    """
    scenic_scores = np.zeros_like(forest)
    for y in range(
        1, forest.shape[0] - 1
    ):  # we can skip the edges, they'll always be 0
        for x in range(1, forest.shape[1] - 1):
            scenic_scores[y, x] = _scenic_score(forest, y, x)
    return scenic_scores.max()


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 8).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
30373
25512
65332
33549
35390
    """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 1560


def test_example_part1(example_input):
    assert part1(example_input) == 21


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 252000


def test_example_part2(example_input):
    assert part2(example_input) == 8
