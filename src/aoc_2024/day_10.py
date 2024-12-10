from collections import defaultdict
from functools import cache
from typing import Any

from aoc.datatypes import Coord, Direction
from aoc.puzzle import PuzzleInput
from frozendict import frozendict
from tqdm import tqdm


def parse_puzzle(
    puzzle: PuzzleInput,
) -> tuple[dict[Coord, int], list[Coord], list[Coord]]:
    topo = {}
    trailheads = []
    ends = []
    for row, line in enumerate(puzzle.lines):
        for col, char in enumerate(line):
            current = Coord(row, col)
            if char == "0":
                trailheads.append(current)
            if char == "9":
                ends.append(current)
            if char == ".":
                continue
            topo[current] = int(char)
    return topo, trailheads, ends


def count_ends(start: Coord, topo: frozendict[Coord, int]):
    seen = set()

    @cache
    def num_trails(start: Coord, topo: frozendict[Coord, int]) -> int:
        if topo[start] == 9:
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
                continue
            if next not in topo:
                continue
            if topo[start] - topo[next] == -1:
                seen.add(next)
                total += num_trails(next, topo)

        return total

    found = num_trails(start, topo)
    return found


def part_1(puzzle: PuzzleInput) -> Any:
    topo, heads, _ = parse_puzzle(puzzle)
    topo_frozen = frozendict(topo)
    total = 0
    for head in tqdm(heads):
        total += count_ends(head, topo_frozen)
    return total


def iterative_increment(topo: dict[Coord, int], ends: list[Coord]) -> dict[Coord, int]:
    to_explore = set(ends)
    moves: dict[Coord, int] = defaultdict(lambda: 0)
    for nine in ends:
        moves[nine] = 1
    for i in range(9, -1, -1):
        next_to_explore = set()
        while to_explore:
            pos = to_explore.pop()
            val = topo[pos]
            if val != i:
                msg = "Something went wrong"
                raise ValueError(msg)

            paths = 0
            for direction in [
                Direction.NORTH,
                Direction.SOUTH,
                Direction.EAST,
                Direction.WEST,
            ]:
                walk = pos + direction
                if walk in topo:
                    if topo[walk] == i + 1:
                        paths += moves[walk]
                    if topo[walk] == i - 1:
                        next_to_explore.add(walk)
            # add to current so 9's stay at 1
            moves[pos] += paths
        to_explore = next_to_explore
    return moves


def get_all_paths(starts: list[Coord], moves: dict[Coord, int]) -> int:
    total = 0
    for start in starts:
        total += moves[start]
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    topo, heads, ends = parse_puzzle(puzzle)
    moves = iterative_increment(topo, ends)
    return get_all_paths(heads, moves)
