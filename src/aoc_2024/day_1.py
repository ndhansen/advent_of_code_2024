from collections import Counter
from typing import Any

from aoc.puzzle import PuzzleInput


def parse_input(puzzle: PuzzleInput) -> tuple[list[int], list[int]]:
    left, right = [], []
    for line in puzzle.lines:
        a, b = line.split("   ", 1)
        left.append(int(a))
        right.append(int(b))
    return left, right


def part_1(puzzle: PuzzleInput) -> Any:
    left, right = parse_input(puzzle)
    left = sorted(left)
    right = sorted(right)
    total = 0
    for a, b in zip(left, right):
        total += abs(a - b)
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    left, right = parse_input(puzzle)
    reference = Counter(right)
    total = 0
    for num in left:
        total += num * reference.get(num, 0)
    return total
