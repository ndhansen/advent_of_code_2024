from typing import Any

from aoc.puzzle import PuzzleInput


def parse(puzzle: PuzzleInput) -> tuple[list[list[int]], list[list[int]]]:
    bs = []
    for block in puzzle.raw.split("\n\n"):
        lines = block.splitlines()
        lines_as_list = list(map(list, lines))
        rotated = list(map(list, zip(*lines_as_list)))
        bs.append(rotated)

    locks = []
    keys = []
    for b in bs:
        fig = []
        for line in b:
            fig.append(line.count("#") - 1)
        if b[0][0] == ".":  # It's a key
            keys.append(fig)
        else:
            locks.append(fig)
    return locks, keys


def part_1(puzzle: PuzzleInput) -> Any:
    locks, keys = parse(puzzle)
    total = 0
    for key in keys:
        for lock in locks:
            combo = []
            fits = True
            for a, b in zip(key, lock):
                if a + b > 5:
                    fits = False
                combo.append(a + b)
            if fits is True:
                total += 1
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    return "✨⭐🌟⭐✨"
