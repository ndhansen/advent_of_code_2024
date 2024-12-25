import itertools
from typing import Any

from aoc.puzzle import PuzzleInput

type Key = list[int]
type Lock = list[int]


def parse(puzzle: PuzzleInput) -> tuple[list[Lock], list[Key]]:
    schematics = []
    for block in puzzle.raw.split("\n\n"):
        lines = block.splitlines()
        lines_as_list = [list(x) for x in lines]
        rotated = [list(x) for x in zip(*lines_as_list)]
        schematics.append(rotated)

    locks = []
    keys = []
    for schematic in schematics:
        fig = []
        for line in schematic:
            fig.append(line.count("#") - 1)
        if schematic[0][0] == ".":  # It's a key
            keys.append(fig)
        else:
            locks.append(fig)
    return locks, keys


def possible_key_combos(locks: list[Lock], keys: list[Key]) -> int:
    total = 0
    for key, lock in itertools.product(keys, locks):
        fits = True
        for bite, pin in zip(key, lock):
            if bite + pin > 5:
                fits = False
        if fits is True:
            total += 1
    return total


def part_1(puzzle: PuzzleInput) -> Any:
    locks, keys = parse(puzzle)
    return possible_key_combos(locks, keys)


def part_2(puzzle: PuzzleInput) -> Any:
    return "✨⭐🌟⭐✨"
