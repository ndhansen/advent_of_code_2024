from typing import Any

import regex as re
from aoc.datatypes import Coord
from aoc.puzzle import PuzzleInput


def get_diagonals(puzzle: PuzzleInput) -> list[str]:
    directions = [Coord(1, 0), Coord(0, 1)]
    diagonals = []
    # left to top
    for y in range(len(puzzle.lines)):
        line = []
        current = Coord(y, 0)
        while current.row >= 0:
            line.append(puzzle.lines[current.row][current.col])
            current += Coord(-1, 1)
        diagonals.append("".join(line))

    # bottom to right
    # 5, 1 -> 4, 2 -> 3, 3 -> ...
    # 5, 2 -> 4, 3 -> 3, 4 -> ...
    for col in range(1, len(puzzle.lines[0])):
        line = []
        current = Coord(len(puzzle.lines) - 1, col)
        while current.col < len(puzzle.lines[0]):
            line.append(puzzle.lines[current.col][current.row])
            current += Coord(-1, 1)
        diagonals.append("".join(line))

    # right to top
    # 0, 5
    # 1, 5 -> 0, 4
    # 2, 5 -> 1, 4 -> 0, 3
    for row in range(len(puzzle.lines)):
        line = []
        current = Coord(row, len(puzzle.lines[0]) - 1)
        while current.row >= 0:
            line.append(puzzle.lines[current.col][current.row])
            current += Coord(-1, -1)
        diagonals.append("".join(line))

    # bottom to left
    # 5, 4 -> 4, 3 -> 3, 2
    # 5, 3 -> 4, 2 -> ...
    for col in range(len(puzzle.lines) - 2, -1, -1):
        line = []
        current = Coord(len(puzzle.lines) - 1, col)
        while current.col >= 0:
            line.append(puzzle.lines[current.col][current.row])
            current += Coord(-1, -1)
        diagonals.append("".join(line))

    # Flip all of them
    all_diagonals = diagonals.copy()
    for diagonal in diagonals:
        all_diagonals.append("".join(reversed(diagonal)))
    return all_diagonals


def get_straigts(puzzle: PuzzleInput) -> list[str]:
    all_lines = []
    all_lines.extend(puzzle.lines.copy())

    for line in puzzle.lines:
        all_lines.append("".join(reversed(line)))

    for col in range(len(puzzle.lines[0])):
        line = []
        for row in range(len(puzzle.lines)):
            line.append(puzzle.lines[row][col])
        all_lines.append("".join(line))
        all_lines.append("".join(reversed(line)))

    return all_lines


def count_xmas(lines: list[str]) -> int:
    pattern = r"(XMAS)"
    total = 0
    for line in lines:
        total += len(re.findall(pattern, line))
    return total


def part_1(puzzle: PuzzleInput) -> Any:
    straights = get_straigts(puzzle)
    diagonals = get_diagonals(puzzle)
    num_straight = count_xmas(straights)
    num_diagonals = count_xmas(diagonals)
    return num_straight + num_diagonals


def find_crosses(puzzle: PuzzleInput, letters: list[str]) -> int:
    dist = len(puzzle.lines[0]) - 1
    pattern = (
        letters[0]
        + r"\S{1}"
        + letters[1]
        + ".{"
        + str(dist)
        + "}A.{"
        + str(dist)
        + "}"
        + letters[2]
        + r"\S{1}"
        + letters[3]
    )
    conjoined = "\n".join(puzzle.lines)
    return len(re.findall(pattern, conjoined, overlapped=True, flags=re.S))


def part_2(puzzle: PuzzleInput) -> Any:
    letter_sets = [
        ["M", "S", "M", "S"],
        ["M", "M", "S", "S"],
        ["S", "M", "S", "M"],
        ["S", "S", "M", "M"],
    ]
    total = 0
    for letters in letter_sets:
        found = find_crosses(puzzle, letters)
        total += found
    return total
