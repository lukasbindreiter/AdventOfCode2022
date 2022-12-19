import re
from functools import lru_cache

import networkx as nx
import pytest
from aocd.models import Puzzle

INPUT_PATTERN = re.compile(
    r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)"
)


def parse(data: str) -> nx.Graph:
    graph = nx.Graph()
    parsed = [
        tuple(INPUT_PATTERN.match(line).groups()) for line in data.strip().splitlines()
    ]
    for valve, flow_rate, _ in parsed:
        graph.add_node(valve, flow_rate=int(flow_rate))

    for valve, _, valves in parsed:
        for target_valve in valves.split(", "):
            graph.add_edge(valve, target_valve, weight=1)

    return _simplify_graph(graph, keep=["AA"])


def _simplify_graph(graph, keep=()):
    """
    Remove nodes with flow_rate=0 that only act as connectors and instead
    connect the ingoing and outgoing nodes directly"""
    graph = graph.copy()
    for node in list(graph.nodes):
        if node in keep or graph.nodes[node]["flow_rate"] > 0:
            continue

        for node_in, in_attrs in graph[node].items():
            for node_out, out_attrs in graph[node].items():
                if node_in != node_out and (node_in, node_out) not in graph.edges:
                    graph.add_edge(
                        node_in,
                        node_out,
                        weight=in_attrs["weight"] + out_attrs["weight"],
                    )

        graph.remove_node(node)
    return graph


class Volcano:
    def __init__(self, distances, flow_rates, start_node):
        self.distances = distances
        self.flow_rates = flow_rates
        self.start_node = start_node

    def __hash__(self):  # values are constant throughout
        return 1234


def part1(graph: nx.Graph) -> int:
    distances = nx.floyd_warshall_numpy(graph).astype(int)
    flow_rates = tuple([graph.nodes[n]["flow_rate"] for n in graph])
    start_node = list(graph).index("AA")
    volcano = Volcano(distances, flow_rates, start_node)

    closed_valves = frozenset(range(len(distances))) - {start_node}
    return exhaustive_search(volcano, start_node, closed_valves, 30, False)


@lru_cache(maxsize=None)
def exhaustive_search(volcano, valve, closed_valves, remaining_time, elephant: bool):
    # 0 as fallback value for the max() below if no more actions are possible
    pressures = [0]

    # try moving to all remaining valves next, continue the search for each one
    # and then return the option with the maximum pressure released at the end
    for next_valve in closed_valves:
        distance = volcano.distances[valve, next_valve]
        if distance > remaining_time:  # can't reach this valve in time
            continue

        # the pressure we can release if we move to that valve and open it
        valve_pressure = volcano.flow_rates[next_valve] * (
            remaining_time - distance - 1
        )

        # continue the search if we move to next_valve, open it and then continue on
        pressures.append(
            valve_pressure
            + exhaustive_search(
                volcano,
                next_valve,
                closed_valves - {next_valve},
                remaining_time - distance - 1,
                elephant,
            )
        )

    # for part2 we also have another option other than moving to a valve and opening it:
    # stop doing anything (we are finished), and let the elephant work on all the
    # remaining valves
    if elephant:
        pressures.append(
            exhaustive_search(volcano, volcano.start_node, closed_valves, 26, False)
        )

    return max(pressures)


def part2(graph: nx.Graph) -> int:
    distances = nx.floyd_warshall_numpy(graph).astype(int)
    flow_rates = tuple([graph.nodes[n]["flow_rate"] for n in graph])
    start_node = list(graph).index("AA")
    volcano = Volcano(distances, flow_rates, start_node)

    closed_valves = frozenset(range(len(distances))) - {start_node}
    return exhaustive_search(volcano, start_node, closed_valves, 26, True)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 16).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
        """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 1474


def test_example_part1(example_input):
    assert part1(example_input) == 1651


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 2100


def test_example_part2(example_input):
    assert part2(example_input) == 1707
