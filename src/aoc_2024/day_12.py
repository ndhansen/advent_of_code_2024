import enum
from typing import Any

from aoc.datatypes import Coord, Direction
from aoc.puzzle import PuzzleInput


def parse(puzzle: PuzzleInput) -> dict[Coord, str]:
    garden = {}
    for row, line in enumerate(puzzle.lines):
        for col, char in enumerate(line):
            garden[Coord(row, col)] = char
    return garden


class Pricing(enum.Enum):
    SIDES = enum.auto()
    PERIMITER = enum.auto()


def flood_fill(garden: dict[Coord, str], pricing: Pricing) -> int:
    to_process = set(garden.keys())
    total = 0
    while to_process:
        current_plot = {to_process.pop()}
        seen = current_plot.copy()
        size = 1
        perimiter: set[tuple[Coord, Coord]] = set()
        while current_plot:
            current = current_plot.pop()
            for direction in [
                Direction.NORTH,
                Direction.SOUTH,
                Direction.WEST,
                Direction.EAST,
            ]:
                neighbor = current + direction
                if neighbor in seen:
                    continue
                elif neighbor not in garden:
                    perimiter.add((current, neighbor))
                    # perimiter += 1
                elif garden[current] == garden[neighbor]:
                    size += 1
                    current_plot.add(neighbor)
                    to_process.discard(neighbor)
                    seen.add(neighbor)
                else:
                    perimiter.add((current, neighbor))
                    # perimiter += 1

        if pricing == Pricing.SIDES:
            sides = 0
            while perimiter:
                adjacent_edges = {perimiter.pop()}
                sides += 1
                while adjacent_edges:
                    current = adjacent_edges.pop()
                    a, b = current
                    for direction in [
                        Direction.NORTH,
                        Direction.SOUTH,
                        Direction.WEST,
                        Direction.EAST,
                    ]:
                        na = a + direction
                        nb = b + direction
                        neighbor = (na, nb)
                        if neighbor in perimiter:
                            adjacent_edges.add(neighbor)
                            perimiter.remove(neighbor)
            total += size * sides
        elif pricing == Pricing.PERIMITER:
            total += size * len(perimiter)

    return total


def part_1(puzzle: PuzzleInput) -> Any:
    garden = parse(puzzle)
    return flood_fill(garden, Pricing.PERIMITER)


def part_2(puzzle: PuzzleInput) -> Any:
    pass
    garden = parse(puzzle)
    return flood_fill(garden, Pricing.SIDES)
