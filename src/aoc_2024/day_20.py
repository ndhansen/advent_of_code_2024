import itertools
import math
from typing import Any, Iterator, Mapping

from aoc.a_star import Cost, Heuristic, Neighbors, a_star
from aoc.datatypes import Coord
from aoc.puzzle import PuzzleInput
from tqdm import tqdm


def parse(puzzle: PuzzleInput) -> tuple[Coord, Coord, Coord, set[Coord]]:
    start = end = None
    maze = set()
    size = Coord(len(puzzle.lines), len(puzzle.lines[0]))
    for row, line in enumerate(puzzle.lines):
        for col, char in enumerate(line):
            current = Coord(row, col)
            match char:
                case "S":
                    start = current
                case "E":
                    end = current
                case "#":
                    maze.add(current)
    if start is None or end is None:
        raise ValueError

    return start, end, size, maze


class MazeHeuristic(Heuristic[Coord]):
    def __call__(self, current: Coord, target: Coord) -> float:
        row_diff = abs((current - target).row)
        col_diff = abs((current - target).col)
        return float(row_diff + col_diff)


class MazeNeighbors(Neighbors[Coord]):
    def __init__(self, maze: set[Coord], size: Coord) -> None:
        self.maze = maze
        self.size = size

    def __call__(self, current: Coord, paths: Mapping[Coord, Coord]) -> Iterator[Coord]:  # noqa: ARG002
        for potential_neighbor in [
            Coord(-1, 0),
            Coord(1, 0),
            Coord(0, -1),
            Coord(0, 1),
        ]:
            neighbor = current + potential_neighbor
            if (
                neighbor.row < 0
                or neighbor.col < 0
                or neighbor.row >= self.size.row
                or neighbor.col >= self.size.col
            ):
                continue
            if neighbor not in self.maze:
                yield neighbor


class MazeCost(Cost[Coord]):
    def __call__(
        self, paths: Mapping[Coord, Coord], current: Coord, last: Coord
    ) -> float:  # noqa: ARG002
        return 1


def get_removable_walls(maze: set[Coord], size: Coord) -> set[Coord]:
    removable = set()
    for wall in maze:
        if (
            wall.row == 0
            or wall.col == 0
            or wall.row == size.row - 1
            or wall.col == size.col - 1
        ):
            continue
        free = 0
        for surrounding in [
            Coord(-1, 0),
            Coord(1, 0),
            Coord(0, -1),
            Coord(0, 1),
        ]:
            current = wall + surrounding
            if current not in maze:
                free += 1

        if free > 1:
            removable.add(wall)
    return removable


def precompute_path(
    start: Coord, end: Coord, size: Coord, maze: set[Coord]
) -> dict[Coord, tuple[int, int]]:
    neighbor_func = MazeNeighbors(maze, size)

    start_path_cache = {}
    end_path_cache = {}

    frontier = {start}
    seen = {start}
    steps = 0
    while frontier:
        next_frontier = set()
        for current in frontier:
            start_path_cache[current] = steps
            for neighbor in neighbor_func(current, {}):
                if neighbor in seen:
                    continue
                next_frontier.add(neighbor)
                seen.add(neighbor)
        frontier = next_frontier
        steps += 1

    frontier = {end}
    seen = {end}
    steps = 0
    while frontier:
        next_frontier = set()
        for current in frontier:
            end_path_cache[current] = steps
            for neighbor in neighbor_func(current, {}):
                if neighbor in seen:
                    continue
                next_frontier.add(neighbor)
                seen.add(neighbor)
        frontier = next_frontier
        steps += 1

    path_cache = {}
    for coord in start_path_cache.keys():
        path_cache[coord] = (start_path_cache[coord], end_path_cache[coord])

    return path_cache


def efficient_wall_removal(
    start: Coord, end: Coord, size: Coord, maze: set[Coord]
) -> int:
    neighbor_func = MazeNeighbors(maze, size)
    heuristic = MazeHeuristic()
    cost_func = MazeCost()
    _, cost = a_star(start, end, heuristic, cost_func, neighbor_func)
    total = 0
    path_cache = precompute_path(start, end, size, maze)
    for removable in tqdm(get_removable_walls(maze, size)):
        lowest_start = lowest_end = math.inf
        for surrounding in [
            Coord(-1, 0),
            Coord(1, 0),
            Coord(0, -1),
            Coord(0, 1),
        ]:
            current = removable + surrounding
            if current not in path_cache:
                continue
            if path_cache[current][0] < lowest_start:
                lowest_start = path_cache[current][0]
            if path_cache[current][1] < lowest_end:
                lowest_end = path_cache[current][1]
        if lowest_start == math.inf or lowest_end == math.inf:
            raise ValueError

        new_cost = lowest_start + lowest_end + 2
        if cost - new_cost >= 100:
            total += 1

    return total


def part_1(puzzle: PuzzleInput) -> Any:
    start, end, size, maze = parse(puzzle)
    return efficient_wall_removal(start, end, size, maze)


def big_cheat(start: Coord, end: Coord, size: Coord, maze: set[Coord]) -> int:
    neighbor_func = MazeNeighbors(maze, size)
    heuristic = MazeHeuristic()
    cost_func = MazeCost()
    _, cost = a_star(start, end, heuristic, cost_func, neighbor_func)
    path_cache = precompute_path(start, end, size, maze)
    total = 0
    for start, end in itertools.permutations(path_cache.keys(), 2):
        dist = abs(start.row - end.row) + abs(start.col - end.col)
        if dist > 20:
            continue

        new_cost = path_cache[start][0] + path_cache[end][1] + dist
        if cost - new_cost >= 100:
            total += 1
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    start, end, size, maze = parse(puzzle)
    return big_cheat(start, end, size, maze)
