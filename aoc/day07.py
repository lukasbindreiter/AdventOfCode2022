from collections import defaultdict

import pytest
from aocd.models import Puzzle


def parse(data: str) -> list[str]:
    return data.strip().splitlines()


def _directory_sizes(lines: list[str]) -> dict[str, int]:
    directory_sizes = defaultdict(int)

    for line in lines:
        match line.split():
            case "$", "cd", "/":
                directories = ["/"]
            case "$", "cd", "..":
                directories.pop()
            case "$", "cd", dir_name:
                directories.append(directories[-1] + dir_name + "/")
            case "$", "ls":
                continue
            case "dir", _:
                continue
            case file_size, _:
                for directory in directories:
                    directory_sizes[directory] += int(file_size)

    return directory_sizes


def part1(lines: list[str]) -> int:
    sizes = _directory_sizes(lines)
    return sum(val for val in sizes.values() if val <= 100000)


def part2(lines: list[str]) -> int:
    sizes = _directory_sizes(lines)

    filesystem_size = 70000000
    required_disk_space = 30000000
    used_disk_space = sizes["/"]

    unused_space = filesystem_size - used_disk_space
    to_delete = required_disk_space - unused_space

    return min(val for val in sizes.values() if val >= to_delete)


@pytest.fixture()
def puzzle_input():
    return parse(Puzzle(2022, 7).input_data)


@pytest.fixture()
def example_input():
    return parse(
        """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
    """
    )


def test_part1(puzzle_input):
    assert part1(puzzle_input) == 1611443


def test_example_part1(example_input):
    assert part1(example_input) == 95437


def test_part2(puzzle_input):
    assert part2(puzzle_input) == 2086088


def test_example_part2(example_input):
    assert part2(example_input) == 24933642
