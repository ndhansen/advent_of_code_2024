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


def parse(puzzle: PuzzleInput) -> list[Machine]:
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
                target=Coord(int(p[1]), int(p[0])),
            )
        )
    return machines


def parse_2(puzzle: PuzzleInput) -> list[Machine]:
    machines = parse(puzzle)
    big_machines = []
    for machine in machines:
        big_machines.append(
            Machine(
                a=machine.a,
                b=machine.b,
                target=Coord(
                    machine.target.row + 10000000000000,
                    machine.target.col + 10000000000000,
                ),
            )
        )
    return big_machines


def bruteforce(machines: list[Machine]) -> int:
    total = 0
    for machine in machines:
        lowest_cost = None
        for a_presses in range(1, 101):
            a_result = Coord(machine.a.row * a_presses, machine.a.col * a_presses)
            if a_result > machine.target:
                break
            for b_presses in range(1, 101):
                b_result = Coord(machine.b.row * b_presses, machine.b.col * b_presses)
                result = a_result + b_result
                if result > machine.target:
                    break
                if result != machine.target:
                    continue

                cost = (3 * a_presses) + b_presses
                if lowest_cost is None:
                    lowest_cost = cost
                elif cost < lowest_cost:
                    lowest_cost = cost

        if lowest_cost is not None:
            total += lowest_cost

    return total


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
    return bruteforce(machines)


def part_2(puzzle: PuzzleInput) -> Any:
    machines = parse_2(puzzle)
    return equation_solve(machines)
