import re
from typing import Any

from aoc.puzzle import PuzzleInput


def part_1(puzzle: PuzzleInput) -> Any:
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    multiplications = []
    for line in puzzle.lines:
        matches = re.findall(pattern, line)
        multiplications.extend(matches)
    total = 0

    for a, b in multiplications:
        total += int(a) * int(b)
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))"
    multiplications = []
    enabled = True
    for line in puzzle.lines:
        matches = re.findall(pattern, line)
        for left, right, enable, disable in matches:
            if left != "" and right != "" and enabled is True:
                multiplications.append((int(left), int(right)))
            elif disable != "":
                enabled = False
            elif enable != "":
                enabled = True

    total = 0
    for a, b in multiplications:
        total += a * b
    return total
