from collections import defaultdict, deque
from typing import Any

from aoc.puzzle import PuzzleInput


def parse(puzzle: PuzzleInput) -> list[int]:
    nums = []
    for line in puzzle.lines:
        nums.append(int(line))
    return nums


def operate(num: int) -> int:
    val = num * 64
    num = num ^ val
    num = num % 16777216

    val = num // 32
    num = num ^ val
    num = num % 16777216

    val = num * 2048
    num = num ^ val
    num = num % 16777216
    return num


def part_1(puzzle: PuzzleInput) -> Any:
    total = 0
    for line in puzzle.lines:
        num = int(line)
        for _ in range(2000):
            num = operate(num)
        total += num
    return total


def get_sequences(num: int) -> dict[tuple[int, int, int, int], int]:
    prices = {}
    old_digit = int(str(num)[-1])
    rolling_window = deque([])
    for _ in range(2000):
        num = operate(num)
        new_digit = int(str(num)[-1])
        change = new_digit - old_digit
        rolling_window.append(change)
        while len(rolling_window) > 4:
            rolling_window.popleft()
        if len(rolling_window) == 4:
            # if new_digit > prices[tuple(rolling_window)]:
            if tuple(rolling_window) not in prices:
                prices[tuple(rolling_window)] = new_digit
        old_digit = new_digit

    return prices


def merge_sequences(nums: list[int]) -> int:
    prices = defaultdict(int)
    for num in nums:
        new_prices = get_sequences(num)
        for k, v in new_prices.items():
            prices[k] += v
    return max(prices.values())


def part_2(puzzle: PuzzleInput) -> Any:
    nums = parse(puzzle)
    return merge_sequences(nums)
