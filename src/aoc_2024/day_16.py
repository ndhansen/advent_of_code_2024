import math
from collections import defaultdict
from collections.abc import Iterator, Mapping
from typing import Any

from aoc.a_star import Cost, Heuristic, Neighbors, a_star
from aoc.datatypes import Coord, Direction
from aoc.exceptions import UnsolveableError
from aoc.puzzle import PuzzleInput
from tqdm import tqdm


class ReindeerHeuristic(Heuristic[Coord]):
    def __call__(self, current: Coord, goal: Coord) -> float:
        return abs(current.row - goal.row) + abs(current.col - goal.col)


class ReindeerNeighbors(Neighbors[Coord]):
    def __init__(self, maze: set[Coord]) -> None:
        self.maze = maze

    def __call__(self, current: Coord, paths: Mapping[Coord, Coord]) -> Iterator[Coord]:
        for direction in (
            Direction.NORTH,
            Direction.SOUTH,
            Direction.EAST,
            Direction.WEST,
        ):
            neighbor = current + direction
            if neighbor in self.maze:
                continue
            if neighbor in paths:
                continue
            yield neighbor


class ReindeerCost(Cost[Coord]):
    def __call__(
        self, paths: Mapping[Coord, Coord], current: Coord, last: Coord
    ) -> float:
        new_facing = current - last
        prior = paths.get(last, last - Coord(0, 1))

        facing = None
        if prior is None:
            facing = Coord(0, 1)
        else:
            facing = last - prior

        if new_facing == facing:
            return 1.0
        return 1001.0


def parse(puzzle: PuzzleInput) -> tuple[set[Coord], Coord, Coord]:
    r = None
    end = None
    walls = set()
    for row, line in enumerate(puzzle.lines):
        for col, char in enumerate(line):
            current = Coord(row, col)
            match char:
                case "S":
                    r = current
                case "E":
                    end = current
                case "#":
                    walls.add(current)
    if r is None or end is None:
        raise ValueError

    return walls, r, end


def part_1(puzzle: PuzzleInput) -> Any:
    maze, start, end = parse(puzzle)
    rh = ReindeerHeuristic()
    rc = ReindeerCost()
    rn = ReindeerNeighbors(maze)
    _, cost = a_star(start, end, rh, rc, rn)
    return int(cost)


def find_all_fastest_wrong(maze: set[Coord], start: Coord, end: Coord) -> int:
    """
    I left this in because it works on the full puzzle input but fails on the tests.
    It's incorrect.
    """
    rh = ReindeerHeuristic()
    rc = ReindeerCost()
    rn = ReindeerNeighbors(maze)
    path, cost = a_star(start, end, rh, rc, rn)
    seen = set(path)
    for i in tqdm(range(1, len(path) - 1)):
        new_maze = maze.copy()
        new_maze.add(path[i])
        rn = ReindeerNeighbors(new_maze)
        try:
            new_path, new_cost = a_star(start, end, rh, rc, rn)
        except UnsolveableError:
            continue

        if new_cost != cost:
            continue

        seen.update(new_path)
    for row in range(15):
        for col in range(15):
            current = Coord(row, col)
            if current in maze:
                print("#", end="")
            elif current in seen:
                print("O", end="")
            else:
                print(".", end="")
    return len(seen)


def part_2_alt(puzzle: PuzzleInput) -> Any:
    maze, start, end = parse(puzzle)
    return find_all_fastest_wrong(maze, start, end)


def bfs(maze: set[Coord], start: Coord, end: Coord, target_cost: int) -> int:
    iterations = [(start, [], Direction.EAST, 0)]
    fastest: dict[tuple[Coord, Direction], float] = defaultdict(lambda: math.inf)
    done = False
    paths = []
    while not done:
        next_iteration = []
        for current, path, dir, cost in iterations:
            if cost > fastest[(current, dir)]:
                continue

            if current == end:
                if cost == target_cost:
                    done = True
                    paths.append([*path, current])
                else:
                    continue

            possibles = []
            if current + dir not in maze:
                possibles.append((current + dir, [*path, current], dir, cost + 1))

            if dir in (Direction.EAST, Direction.WEST):
                possibles.append((current, path, Direction.NORTH, cost + 1000))
                possibles.append((current, path, Direction.SOUTH, cost + 1000))
            else:
                possibles.append((current, path, Direction.EAST, cost + 1000))
                possibles.append((current, path, Direction.WEST, cost + 1000))

            for p in possibles:
                if fastest[(p[0], p[2])] >= p[3]:
                    fastest[(p[0], p[2])] = p[3]
                    next_iteration.append(p)

        iterations = next_iteration

    all_paths = set()
    for path in paths:
        all_paths.update(set(path))
    for row in range(15):
        for col in range(15):
            current = Coord(row, col)
            if current in maze:
                print("#", end="")
            elif current in all_paths:
                print("O", end="")
            else:
                print(".", end="")
        print()
    return len(all_paths)


def part_2(puzzle: PuzzleInput) -> Any:
    maze, start, end = parse(puzzle)
    rh = ReindeerHeuristic()
    rc = ReindeerCost()
    rn = ReindeerNeighbors(maze)
    _, cost = a_star(start, end, rh, rc, rn)
    return bfs(maze, start, end, int(cost))
