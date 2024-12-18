from collections.abc import Iterator
from typing import Any, Mapping

from aoc.a_star import Cost, Heuristic, Neighbors, a_star
from aoc.datatypes import Coord
from aoc.exceptions import UnsolveableError
from aoc.puzzle import PuzzleInput


def parse_1(puzzle: PuzzleInput) -> tuple[set[Coord], Coord]:
    if puzzle.test:
        size = Coord(7, 7)
        cutoff = 12
    else:
        size = Coord(71, 71)
        cutoff = 1024

    maze = set()
    for line in puzzle.lines[:cutoff]:
        x, y = line.split(",", 1)
        current = Coord(int(y), int(x))
        maze.add(current)

    return maze, size


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
            if neighbor not in self.maze and neighbor not in paths:
                yield neighbor


class MazeCost(Cost[Coord]):
    def __call__(
        self, paths: Mapping[Coord, Coord], current: Coord, last: Coord
    ) -> float:  # noqa: ARG002
        return 1


def part_1(puzzle: PuzzleInput) -> Any:
    maze, size = parse_1(puzzle)
    heuristic = MazeHeuristic()
    neighbor_func = MazeNeighbors(maze, size)
    cost_func = MazeCost()
    _, cost = a_star(
        Coord(0, 0), size - Coord(1, 1), heuristic, cost_func, neighbor_func
    )
    return int(cost)


def get_size(puzzle) -> Coord:
    if puzzle.test:
        return Coord(7, 7)
    return Coord(71, 71)


def get_memory_block(puzzle: PuzzleInput) -> Iterator[Coord]:
    for i in range(len(puzzle.lines)):
        for line in puzzle.lines[:i]:
            x, y = line.split(",", 1)
            current = Coord(int(y), int(x))
            yield current


def part_2(puzzle: PuzzleInput) -> Any:
    size = get_size(puzzle)
    heuristic = MazeHeuristic()
    cost_func = MazeCost()
    maze = set()
    last_path = None
    for block in get_memory_block(puzzle):
        maze.add(block)
        if last_path is not None and block not in last_path:
            continue

        neighbor_func = MazeNeighbors(maze, size)
        try:
            last_path, _ = a_star(
                Coord(0, 0), size - Coord(1, 1), heuristic, cost_func, neighbor_func
            )
        except UnsolveableError:
            return str(block.col) + "," + str(block.row)
