from collections import defaultdict
from functools import cache
from typing import Any

from aoc.datatypes import Coord, Direction
from aoc.puzzle import PuzzleInput
from frozendict import frozendict
from tqdm import tqdm


def parse_puzzle(puzzle: PuzzleInput) -> tuple[dict[Coord, int], list[Coord]]:
    topo = {}
    trailheads = []
    for row, line in enumerate(puzzle.lines):
        for col, char in enumerate(line):
            current = Coord(row, col)
            if char == "0":
                trailheads.append(current)
            if char == ".":
                continue
            topo[current] = int(char)
    return topo, trailheads


def count_ends(start: Coord, topo: frozendict[Coord, int]):
    seen: dict[Coord, int] = defaultdict(int)
    seen2 = set()

    @cache
    def num_trails(start: Coord, topo: frozendict[Coord, int]) -> int:
        if topo[start] == 9:
            seen[start] = 1
            return 1

        total = 0
        for direction in [
            Direction.NORTH,
            Direction.SOUTH,
            Direction.EAST,
            Direction.WEST,
        ]:
            next = start + direction
            if next in seen:
                total += seen[next]
                continue
            if next not in topo:
                continue
            if topo[start] - topo[next] == -1:
                total += num_trails(next, topo)

        seen[start] = total
        return total

    found = num_trails(start, topo)
    print(f"{start}: found {seen[start]}")
    import pudb

    pudb.set_trace()
    return seen[start]


def part_1(puzzle: PuzzleInput) -> Any:
    topo, heads = parse_puzzle(puzzle)
    topo_frozen = frozendict(topo)
    total = 0
    # import pudb
    #
    # pudb.set_trace()
    for head in tqdm(heads):
        total += count_ends(head, topo_frozen)
        # print(found)
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    # 3618 too high
    pass
