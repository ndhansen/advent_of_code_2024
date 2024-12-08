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


def get_antinodes(grid: dict[str, set[Coord]], size: Coord) -> int:
    all_antinodes: list[Coord] = []
    for char in grid.keys():
        for first, second in itertools.combinations(grid[char], 2):
            diff = first - second
            all_antinodes.append(first + diff)
            all_antinodes.append(second - diff)

    print(all_antinodes)
    in_bound_antinodes = []
    for node in all_antinodes:
        if (
            node.row >= 0
            and node.row < size.row
            and node.col >= 0
            and node.col < size.col
        ):
            in_bound_antinodes.append(node)

    print(in_bound_antinodes)
    show(in_bound_antinodes, size)
    return len(set(in_bound_antinodes))


def show(nodes: list[Coord], size: Coord):
    for row in range(size.row):
        for col in range(size.col):
            if Coord(row, col) in nodes:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part_1(puzzle: PuzzleInput) -> Any:
    grid = parse_puzzle(puzzle)
    size = get_size(puzzle)
    return get_antinodes(grid, size)


def part_2(puzzle: PuzzleInput) -> Any:
    pass
