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
    seen = set()

    @cache
    def num_trails(start: Coord, topo: frozendict[Coord, int]) -> frozenset[Coord]:
        if topo[start] == 9:
            return frozenset([start])

        ends = []
        for direction in [
            Direction.NORTH,
            Direction.SOUTH,
            Direction.EAST,
            Direction.WEST,
        ]:
            next = start + direction
            if next in seen:
                continue
            if next not in topo:
                continue
            if topo[start] - topo[next] == -1:
                seen.add(next)
                next_heads = num_trails(next, topo)
                for h in next_heads:
                    ends.append(h)

        return frozenset(ends)

    found = len(num_trails(start, topo))
    print(f"{start}: found {found}")
    return found


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
    pass
