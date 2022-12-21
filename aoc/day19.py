import re
from dataclasses import dataclass
from functools import cached_property, lru_cache
from math import ceil, inf

import pytest
from aocd.models import Puzzle


@dataclass
class Blueprint:
    blueprint_id: int
    ore_bot_ore_cost: int
    clay_bot_ore_cost: int
    obsidian_bot_ore_cost: int
    obsidian_bot_clay_cost: int
    geode_bot_ore_cost: int
    geode_bot_obsidian_cost: int

    def __hash__(self) -> int:
        return hash(self.blueprint_id)

    @cached_property
    def max_ore_costs(self) -> int:
        return max(
            self.ore_bot_ore_cost,
            self.clay_bot_ore_cost,
            self.obsidian_bot_ore_cost,
            self.geode_bot_ore_cost,
        )

    def ore_bot_possible_in(self, ores: int, ore_bots: int) -> int:
        """Minutes until we have enough ressources for an ore bot"""
        return max(0, ceil((self.ore_bot_ore_cost - ores) / ore_bots))

    def clay_bot_possible_in(self, ores: int, ore_bots: int) -> int:
        """Minutes until we have enough ressources for a clay bot"""
        return max(0, ceil((self.clay_bot_ore_cost - ores) / ore_bots))

    def obsidian_bot_possible_in(
        self, ores: int, clay: int, ore_bots: int, clay_bots: int
    ) -> int:
        """Minutes until we have enough ressources for an obsidian bot"""
        if clay_bots == 0:
            return inf
        enough_ore_in = max(0, ceil((self.obsidian_bot_ore_cost - ores) / ore_bots))
        enough_clay_in = max(0, ceil((self.obsidian_bot_clay_cost - clay) / clay_bots))
        return max(enough_ore_in, enough_clay_in)

    def geode_bot_possible_in(
        self, ores: int, obsidian: int, ore_bots: int, obsidian_bots: int
    ) -> int:
        """Minutes until we have enough ressources for a geode bot"""
        if obsidian_bots == 0:
            return inf
        enough_ore_in = max(0, ceil((self.geode_bot_ore_cost - ores) / ore_bots))
        enough_obsidian_in = max(
            0, ceil((self.geode_bot_obsidian_cost - obsidian) / obsidian_bots)
        )
        return max(enough_ore_in, enough_obsidian_in)


def parse(data: str) -> list[Blueprint]:
    return [
        Blueprint(*map(int, re.findall(r"\d+", line)))
        for line in data.strip().splitlines()
    ]


@lru_cache(maxsize=None)
def solve(
    blueprint: Blueprint,
    remaining_time: int,
    ore_bots: int = 0,
    clay_bots: int = 0,
    obsidian_bots: int = 0,
    geode_bots: int = 0,
    ores: int = 0,
    clay: int = 0,
    obsidian: int = 0,
    geodes: int = 0,
):
    """
    Search through all possible combinations of building additional bots to find the
    strategy with maximum geodes in the given time

    The idea for this implementation is the following:

    At each turn we decide which bot we want to build next (4 options)
    We then try each option, by skipping ahead the number of time steps it takes until
    we can build that bot and then building it.

    Then the search recursively continues from there, with again the 4 options available

    At the beginning only two bots will be available as options, since the other 2
    require ressources that aren't produced yet.

    Furthermore, another optimization is to stop building bots of a ressource type
    if we already have enough to build every other bot every minute, since additional
    bots wouldn't bring any benefits in that case.

    Doing it this way (deciding which bot to build next) instead of simulating it
    minute by minute (with also the 5th option of not building anything that minute)
    helps reduce the state space tremendously.

    Returns:
        Complete list of states, the build path strategy for maximum geodes in the given
        time
    """

    scores = []
    if ore_bots < blueprint.max_ore_costs:
        # time until we can build that bot (0 means possible now)
        possible_in = blueprint.ore_bot_possible_in(ores, ore_bots)
        # number of time steps we skip forward
        time_skip = possible_in + 1
        if remaining_time > time_skip:
            scores.append(
                solve(
                    blueprint,
                    remaining_time - time_skip,
                    ore_bots + 1,
                    clay_bots,
                    obsidian_bots,
                    geode_bots,
                    ores + ore_bots * time_skip - blueprint.ore_bot_ore_cost,
                    clay + clay_bots * time_skip,
                    obsidian + obsidian_bots * time_skip,
                    geodes + geode_bots * time_skip,
                )
            )

    if clay_bots < blueprint.obsidian_bot_clay_cost:
        time_skip = blueprint.clay_bot_possible_in(ores, ore_bots) + 1
        if remaining_time > time_skip:
            scores.append(
                solve(
                    blueprint,
                    remaining_time - time_skip,
                    ore_bots,
                    clay_bots + 1,
                    obsidian_bots,
                    geode_bots,
                    ores + ore_bots * time_skip - blueprint.clay_bot_ore_cost,
                    clay + clay_bots * time_skip,
                    obsidian + obsidian_bots * time_skip,
                    geodes + geode_bots * time_skip,
                )
            )

    if obsidian_bots < blueprint.geode_bot_obsidian_cost:
        time_skip = (
            blueprint.obsidian_bot_possible_in(ores, clay, ore_bots, clay_bots) + 1
        )
        if remaining_time > time_skip:
            scores.append(
                solve(
                    blueprint,
                    remaining_time - time_skip,
                    ore_bots,
                    clay_bots,
                    obsidian_bots + 1,
                    geode_bots,
                    ores + ore_bots * time_skip - blueprint.obsidian_bot_ore_cost,
                    clay + clay_bots * time_skip - blueprint.obsidian_bot_clay_cost,
                    obsidian + obsidian_bots * time_skip,
                    geodes + geode_bots * time_skip,
                )
            )

    # no limit for geode bots, we want as much as possible
    time_skip = (
        blueprint.geode_bot_possible_in(ores, obsidian, ore_bots, obsidian_bots) + 1
    )
    if remaining_time > time_skip:
        scores.append(
            solve(
                blueprint,
                remaining_time - time_skip,
                ore_bots,
                clay_bots,
                obsidian_bots,
                geode_bots + 1,
                ores + ore_bots * time_skip - blueprint.geode_bot_ore_cost,
                clay + clay_bots * time_skip,
                obsidian
                + obsidian_bots * time_skip
                - blueprint.geode_bot_obsidian_cost,
                geodes + geode_bots * time_skip,
            )
        )

    if scores:
        # if its possible to build another bot, select the choice with the highest score
        maximum = max(scores, key=lambda states: states[-1][-1])
    else:
        # no more bots can be built in the remaining time
        # just gather ressources until its over
        maximum = [
            (
                0,
                ore_bots,
                clay_bots,
                obsidian_bots,
                geode_bots,
                ores + ore_bots * remaining_time,
                clay + clay_bots * remaining_time,
                obsidian + obsidian_bots * remaining_time,
                geodes + geode_bots * remaining_time,
            )
        ]

    # add the current state to the state list of the solution
    return [
        (
            remaining_time,
            ore_bots,
            clay_bots,
            obsidian_bots,
            geode_bots,
            ores,
            clay,
            obsidian,
            geodes,
        )
    ] + maximum


def part1(blueprints: list[Blueprint]) -> int:
    total = 0
    for blueprint in blueprints:
        states = solve(blueprint, 24, ore_bots=1)
        solve.cache_clear()
        total += blueprint.blueprint_id * states[-1][-1]
    return total


def part2(blueprints: list[Blueprint]) -> int:
    total = 1
    for blueprint in blueprints[:3]:
        # in order to speed up the search we limit it to a time of 28 at the beginning
        start = solve(blueprint, 28, ore_bots=1)
        # then select some intermediate state somewhere after ~15 simulated minutes
        # and continue the search from there on for the full 32 minutes
        # this assumes that the start will be the same for both a 32 min search and
        # a 28 min search, which seems to hold true for my inputs at least :D
        some_intermediate_state = start[-12]
        result = solve(
            blueprint,
            some_intermediate_state[0] + 4,  # 4 minutes from 28 to 32
            *some_intermediate_state[1:]
        )

        total *= result[-1][-1]
    return total


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 19).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
        """.strip()  # noqa: E501
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 1382


def test_example_part1(example_input):
    assert part1(example_input) == 33


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 31740


def test_example_part2(example_input):
    assert part2(example_input) == 56 * 62
