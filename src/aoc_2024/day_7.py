import itertools
from collections.abc import Callable
from operator import add, mul
from typing import Any

from aoc.puzzle import PuzzleInput
from tqdm import tqdm


def parse_input(puzzle: PuzzleInput) -> list[tuple[int, list[int]]]:
    equations = []
    for line in puzzle.lines:
        target_str, rest = line.split(": ", 1)
        target = int(target_str)
        nums = [int(x) for x in rest.split()]
        equations.append((target, nums))
    return equations


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def insert_operators(
    target: int, nums: list[int], functions: tuple[Callable[[int, int], int], ...]
) -> bool:
    for operations in itertools.product(functions, repeat=len(nums) - 1):
        current = nums[0]
        for idx, i in enumerate(nums[1:]):
            current = operations[idx](current, i)
            if current > target:
                break

        if current == target:
            return True
    return False


def count_possible(
    equations: list[tuple[int, list[int]]],
    functions: tuple[Callable[[int, int], int], ...],
) -> int:
    total = 0
    for target, nums in tqdm(equations):
        if insert_operators(target, nums, functions) is True:
            total += target

    return total


def part_1(puzzle: PuzzleInput) -> Any:
    equations = parse_input(puzzle)
    return count_possible(equations, (mul, add))


def part_2(puzzle: PuzzleInput) -> Any:
    equations = parse_input(puzzle)
    return count_possible(equations, (mul, concat, add))
