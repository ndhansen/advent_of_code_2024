from collections import defaultdict
from typing import Any

from aoc.datatypes import Coord, itertools
from aoc.puzzle import PuzzleInput


def parse_puzzle(puzzle: PuzzleInput) -> dict[str, set[Coord]]:
    grid = defaultdict(set)
    for row, line in enumerate(puzzle.lines):
        for col, char in enumerate(line):
            if char != ".":
                grid[char].add(Coord(row, col))
    return grid


def get_size(puzzle: PuzzleInput) -> Coord:
    return Coord(row=len(puzzle.lines), col=len(puzzle.lines[0]))


def get_antinodes(
    grid: dict[str, set[Coord]], size: Coord, part_2: bool = False
) -> int:
    all_antinodes: set[Coord] = set()
    for char in grid.keys():
        for first, second in itertools.combinations(grid[char], 2):
            diff = first - second
            if part_2 is True:
                for i in range(size.row):
                    all_antinodes.add(first + (diff * i))
                    all_antinodes.add(second - (diff * i))
            else:
                all_antinodes.add(first + diff)
                all_antinodes.add(second - diff)

    in_bound_antinodes = []
    for node in all_antinodes:
        if (
            node.row >= 0
            and node.row < size.row
            and node.col >= 0
            and node.col < size.col
        ):
            in_bound_antinodes.append(node)

    return len(set(in_bound_antinodes))


def part_1(puzzle: PuzzleInput) -> Any:
    grid = parse_puzzle(puzzle)
    size = get_size(puzzle)
    return get_antinodes(grid, size)


def part_2(puzzle: PuzzleInput) -> Any:
    grid = parse_puzzle(puzzle)
    size = get_size(puzzle)
    return get_antinodes(grid, size, part_2=True)
