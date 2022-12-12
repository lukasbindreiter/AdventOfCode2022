import networkx as nx
import numpy as np
import pytest
from aocd.models import Puzzle


def _to_height(ch: str) -> int:
    if ch == "S":
        return _to_height("a")
    if ch == "E":
        return _to_height("z")
    return ord(ch) - ord("a")


def parse(data: str) -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
    matrix = np.asarray([list(line) for line in data.split("\n")])
    start = np.where(matrix == "S")
    start = (start[0].item(), start[1].item())
    end = np.where(matrix == "E")
    end = (end[0].item(), end[1].item())
    heights = np.vectorize(_to_height)(matrix)
    return heights, start, end


def part1(heights: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> int:
    graph = nx.grid_2d_graph(*heights.shape).to_directed()
    edges = [
        (src, dst) for src, dst in graph.edges if (heights[src] + 1) >= heights[dst]
    ]
    graph = graph.edge_subgraph(edges)
    return nx.dijkstra_path_length(graph, start, end)


def part2(heights: np.ndarray, _: tuple[int, int], end: tuple[int, int]) -> int:
    graph = nx.grid_2d_graph(*heights.shape).to_directed()
    # we will search from the target node in reverse to all starts -> reverse edges
    edges = [
        (src, dst) for src, dst in graph.edges if (heights[dst] + 1) >= heights[src]
    ]
    graph = graph.edge_subgraph(edges)
    lengths = nx.multi_source_dijkstra_path_length(graph, [end])
    starts = [(y, x) for y, x in zip(*np.where(heights == 0))]
    return min(lengths[s] for s in starts if s in lengths)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 12).input_data)


def test_part1(puzzle_input):
    assert part1(*puzzle_input) == 520


def test_part2(puzzle_input):
    assert part2(*puzzle_input) == 508
