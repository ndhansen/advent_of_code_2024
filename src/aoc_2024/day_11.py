from collections import defaultdict
from typing import Any

from aoc.puzzle import PuzzleInput


def parse(p: PuzzleInput):
    return [int(x) for x in p.lines[0].split(" ")]


def stone_change(number: int) -> list[int]:
    if number == 0:
        return [1]
    if len(str(number)) % 2 == 0:
        mid = len(str(number)) // 2
        left, right = str(number)[:mid], str(number)[mid:]
        return [int(left), int(right)]
    return [2024 * number]


def blink(nums: list[int], counter: int) -> int:
    current = defaultdict(int)
    for num in nums:
        current[num] += 1

    for _ in range(counter):
        new_counts = defaultdict(int)
        for num, count in current.items():
            new_nums = stone_change(num)
            for new_num in new_nums:
                new_counts[new_num] += count
        current = new_counts

    return sum(current.values())


def part_1(puzzle: PuzzleInput) -> Any:
    nums = parse(puzzle)
    return blink(nums, 25)


def part_2(puzzle: PuzzleInput) -> Any:
    nums = parse(puzzle)
    return blink(nums, 75)
