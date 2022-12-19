# thanks shapely for doing all the heavy lifting for this puzzle :)
import re

import pytest
from aocd.models import Puzzle
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union

INPUT_PATTERN = re.compile(
    r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)"
)


def parse(data: str) -> list[Polygon]:
    """Parse sensor coverage areas as shapely polygons"""
    polys = []
    for line in data.strip().splitlines():
        x, y, beacon_x, beacon_y = map(int, re.match(INPUT_PATTERN, line).groups())
        r = abs(x - beacon_x) + abs(y - beacon_y)
        polys.append(Polygon([(x, y - r), (x - r, y), (x, y + r), (x + r, y)]))
    return polys


def part1(sensors: list[Polygon], row: int) -> int:
    # unary_union: intersection of all individual polygons as a single polygon
    sensor_coverage = unary_union(sensors)
    min_x, _, max_x, _ = sensor_coverage.bounds

    # now construct a line at the given row, intersect it with the sensor coverage poly
    # and then just return its length
    line = LineString([(min_x, row), (max_x, row)])
    return int(sensor_coverage.intersection(line).length)


def part2(sensors: list[Polygon]) -> int:
    # with shapely this becomes stupidly easy:
    sensor_coverage = unary_union(sensors)
    # now there is one hole, whose center we can get very easily:
    x, y = sensor_coverage.interiors[0].centroid.coords[0]
    return int(4000000 * x + y)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 15).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
        """.strip()
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input, 2000000) == 4748135


def test_example_part1(example_input):
    assert part1(example_input, 10) == 26


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 13743542639657


def test_example_part2(example_input):
    assert part2(example_input) == 56000011
