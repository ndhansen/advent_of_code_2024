import functools
from typing import Any

from aoc.puzzle import PuzzleInput
from tqdm import tqdm


def parse(puzzle: PuzzleInput) -> tuple[list[str], list[str]]:
    towels = []
    for towel in puzzle.lines[0].split(", "):
        towels.append(towel)

    patterns = puzzle.lines[2:].copy()
    return towels, patterns


@functools.cache
def towel_possible(pattern: str, towels: tuple[str]) -> bool:
    if len(pattern) == 0:
        return True
    for towel in towels:
        if pattern.startswith(towel):
            slice = pattern[len(towel) :]
            if towel_possible(slice, towels):
                return True
    return False


def towels_possible(patterns: list[str], towels: list[str]) -> int:
    total = 0
    for pattern in tqdm(patterns):
        if towel_possible(pattern, tuple(towels)):
            total += 1

    return total


def relevant_towels(towels: list[str]) -> list[str]:
    single_letter_towels = {x for x in towels if len(x) == 1}
    remaining = [x for x in towels if not set(x).issubset(single_letter_towels)]

    remaining.sort(key=len)
    i = 0
    while i < len(remaining):
        t = i + 1
        while t < len(remaining):
            target = remaining[t]
            if remaining[i] in target:
                target = "".join(target.split(remaining[i]))
            if set(target).issubset(single_letter_towels):
                remaining.pop(t)
            else:
                t += 1

        i += 1
    return list(single_letter_towels) + remaining


def part_1(puzzle: PuzzleInput) -> Any:
    towels, patterns = parse(puzzle)
    relevant = relevant_towels(towels)
    return towels_possible(patterns, relevant)


@functools.cache
def towel_permutations(pattern: str, towels: tuple[str]) -> int:
    if len(pattern) == 0:
        return 1
    total = 0
    for towel in towels:
        if pattern.startswith(towel):
            slice = pattern[len(towel) :]
            total += towel_permutations(slice, towels)
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    towels, patterns = parse(puzzle)
    relevant = relevant_towels(towels)
    total = 0
    for pattern in tqdm(patterns):
        if towel_possible(pattern, tuple(relevant)) is not None:
            total += towel_permutations(pattern, tuple(towels))
    return total
