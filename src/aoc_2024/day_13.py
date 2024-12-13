import re
from typing import Any, NamedTuple

from aoc.datatypes import Coord
from aoc.puzzle import PuzzleInput
from sympy import Eq, solve
from sympy.abc import a, b


class Machine(NamedTuple):
    a: Coord
    b: Coord
    target: Coord


def parse(puzzle: PuzzleInput, extra_target: int = 0) -> list[Machine]:
    machines = []
    button_pattern = r".*X\+(\d+), Y\+(\d+).*"
    prize_pattern = r".*X=(\d+), Y=(\d+).*"
    for segment in puzzle.raw.split("\n\n"):
        block = segment.split("\n")
        b1 = re.findall(button_pattern, block[0])[0]
        b2 = re.findall(button_pattern, block[1])[0]
        p = re.findall(prize_pattern, block[2])[0]
        machines.append(
            Machine(
                a=Coord(int(b1[1]), int(b1[0])),
                b=Coord(int(b2[1]), int(b2[0])),
                target=Coord(int(p[1]) + extra_target, int(p[0]) + extra_target),
            )
        )
    return machines


def equation_solve(machines: list[Machine]) -> int:
    total = 0
    for machine in machines:
        solution = solve(
            [
                Eq(a * machine.a.row + b * machine.b.row, machine.target.row),
                Eq(a * machine.a.col + b * machine.b.col, machine.target.col),
            ]
        )
        if not solution[a].is_Integer or not solution[b].is_Integer:
            continue

        total += 3 * int(solution[a]) + int(solution[b])
    return total


def part_1(puzzle: PuzzleInput) -> Any:
    machines = parse(puzzle)
    return equation_solve(machines)


def part_2(puzzle: PuzzleInput) -> Any:
    machines = parse(puzzle, 10000000000000)
    return equation_solve(machines)
