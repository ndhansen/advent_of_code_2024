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


def unjoin(a: int, b: int) -> int:
    if not str(a).endswith(str(b)):
        msg = f"The digits of {b} must occur in that order at the end of {a}"
        raise ValueError(msg)
    return a // 10 ** (len(str(b)))


def solve_recursive(target: int, nums: list[int], joins: bool = False) -> bool:
    if target < 0:
        return False

    if len(nums) == 1:
        if nums[0] == target:
            return True
        return False

    possible_targets = [target - nums[-1]]

    if joins is True and str(target).endswith(str(nums[-1])):
        possible_targets.append(unjoin(target, nums[-1]))

    if target % nums[-1] == 0:
        possible_targets.append(target // nums[-1])

    return any(solve_recursive(t, nums[:-1], joins=joins) for t in possible_targets)


def count_possible(equations: list[tuple[int, list[int]]], joins: bool = False) -> int:
    total = 0
    for target, nums in tqdm(equations):
        if solve_recursive(target, nums, joins=joins) is True:
            total += target

    return total


def part_1(puzzle: PuzzleInput) -> Any:
    equations = parse_input(puzzle)
    return count_possible(equations, joins=False)


def part_2(puzzle: PuzzleInput) -> Any:
    equations = parse_input(puzzle)
    return count_possible(equations, joins=True)
