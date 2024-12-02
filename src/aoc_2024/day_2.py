from typing import Any

from aoc.puzzle import PuzzleInput


def parse_input(puzzle: PuzzleInput) -> list[list[int]]:
    reports = []
    for line in puzzle.lines:
        items = line.split(" ")
        reports.append([int(x) for x in items])
    return reports


def is_safe(report: list[int]) -> bool:
    diffs = []
    for i in range(len(report) - 1):
        diffs.append(report[i] - report[i + 1])

    all_increasing = True
    for i in diffs:
        if i < 1 or i > 3:
            all_increasing = False
    if all_increasing is True:
        return True

    all_decreasing = True
    for i in diffs:
        if i < -3 or i > -1:
            all_decreasing = False
    if all_decreasing is True:
        return True
    return False


def part_1(puzzle: PuzzleInput) -> Any:
    reports = parse_input(puzzle)
    total = 0
    for report in reports:
        total += is_safe(report)
    return total


def is_mostly_safe(report: list[int]) -> bool:
    if is_safe(report):
        return True

    for i in range(len(report)):
        without = report.copy()
        del without[i]
        if is_safe(without) is True:
            return True
    return False


def part_2(puzzle: PuzzleInput) -> Any:
    reports = parse_input(puzzle)
    total = 0
    for report in reports:
        print(is_mostly_safe(report))
        total += is_mostly_safe(report)
    return total
