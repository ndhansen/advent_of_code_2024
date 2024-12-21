import itertools
from collections.abc import Iterator, Mapping
from functools import cache
from typing import Any

from aoc.a_star import Cost, Heuristic, Neighbors, a_star
from aoc.datatypes import Coord
from aoc.puzzle import PuzzleInput

DOOR_KEYPAD = {
    "A": Coord(row=3, col=2),
    "0": Coord(row=3, col=1),
    "1": Coord(row=2, col=0),
    "2": Coord(row=2, col=1),
    "3": Coord(row=2, col=2),
    "4": Coord(row=1, col=0),
    "5": Coord(row=1, col=1),
    "6": Coord(row=1, col=2),
    "7": Coord(row=0, col=0),
    "8": Coord(row=0, col=1),
    "9": Coord(row=0, col=2),
}


ROBOT_KEYPAD = {
    "^": Coord(row=0, col=1),
    "A": Coord(row=0, col=2),
    "<": Coord(row=1, col=0),
    "v": Coord(row=1, col=1),
    ">": Coord(row=1, col=2),
}


class KeypadHeuristic(Heuristic[Coord]):
    def __call__(self, current: Coord, target: Coord) -> float:
        row_diff = abs((current - target).row)
        col_diff = abs((current - target).col)
        return float(row_diff + col_diff)


class KeypadCost(Cost[Coord]):
    def __call__(
        self, paths: Mapping[Coord, Coord], current: Coord, last: Coord
    ) -> float:  # noqa: ARG002
        return 1


class KeypadNeighbors(Neighbors[Coord]):
    def __init__(self, keypad: dict[str, Coord]) -> None:
        self.keypad = set(keypad.values())

    def __call__(self, current: Coord, paths: Mapping[Coord, Coord]) -> Iterator[Coord]:  # noqa: ARG002
        for potential_neighbor in [
            Coord(-1, 0),
            Coord(1, 0),
            Coord(0, -1),
            Coord(0, 1),
        ]:
            neighbor = current + potential_neighbor
            if neighbor in self.keypad:
                yield neighbor


@cache
def is_valid_path(start: Coord, path: tuple[Coord], keypad: frozenset[Coord]) -> bool:
    current = start
    for instruction in path:
        current += instruction
        if current not in keypad:
            return False
    return True


def path_to_possible_instructions(
    path: list[Coord], keypad: dict[str, Coord]
) -> list[list[str]]:
    if len(path) == 1:
        return [["A"]]

    relative = []
    for a, b in itertools.pairwise(path):
        relative.append(b - a)

    test = set()
    test.add(tuple(sorted(relative, reverse=True)))
    test.add(tuple(sorted(relative)))

    possible = set()
    # for possible_path in itertools.permutations(relative, len(relative)):
    for possible_path in test:
        if is_valid_path(path[0], possible_path, frozenset(keypad.values())):
            possible.add(possible_path)

    instructions = []
    for pp in possible:
        current = []
        for x in pp:
            match x:
                case Coord(0, 1):
                    current.append(">")
                case Coord(0, -1):
                    current.append("<")
                case Coord(1, 0):
                    current.append("v")
                case Coord(-1, 0):
                    current.append("^")
        current.append("A")
        instructions.append(current)
    return instructions


def precomputed_paths(
    keypad: dict[str, Coord],
) -> dict[tuple[str, str], list[list[str]]]:
    paths = {}

    neighbor_func = KeypadNeighbors(keypad)
    heuristic = KeypadHeuristic()
    cost_func = KeypadCost()
    for start, goal in itertools.product(keypad.keys(), repeat=2):
        s_coord = keypad[start]
        g_coord = keypad[goal]
        path, _ = a_star(s_coord, g_coord, heuristic, cost_func, neighbor_func)
        instructions = path_to_possible_instructions(path, keypad)
        paths[(start, goal)] = instructions

    return paths


def process_code(code: list[str], robots: int) -> list[str]:
    keypad_paths = precomputed_paths(DOOR_KEYPAD)
    instructions = []
    for start, goal in itertools.pairwise(["A", *code]):
        instructions.append(keypad_paths[(start, goal)])

    possibles = []
    possibles_all = list(itertools.product(*instructions))
    for p_a in possibles_all:
        possibles.append(list(itertools.chain(*p_a)))

    robot_paths = precomputed_paths(ROBOT_KEYPAD)
    for _ in range(robots):
        new_possibles = []
        for possible in possibles:
            temp = []
            for start, goal in itertools.pairwise(["A", *possible]):
                temp.append(robot_paths[(start, goal)])

            temp_all = list(itertools.product(*temp))
            for t_a in temp_all:
                new_possibles.append(list(itertools.chain(*t_a)))

        # possibles = list(itertools.product(*new_possibles))
        new_possibles.sort(key=len)
        shortest = len(new_possibles[0])
        i = len(new_possibles) - 1
        while i > 0:
            if len(new_possibles[i]) > shortest:
                new_possibles.pop(i)
            i -= 1

        # import pudb
        #
        # pudb.set_trace()

        possibles = new_possibles

    return possibles[0]


def calc_score(code: str, path: list[str]) -> int:
    val_str = "".join([char for char in code if char.isnumeric()])
    val = int(val_str)
    return val * len(path)


def part_1(puzzle: PuzzleInput) -> Any:
    total = 0
    for line in puzzle.lines:
        path = process_code(list(line), robots=2)
        print(line, ":", "".join(path), len(path))
        total += calc_score(line, path)
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    total = 0
    for line in puzzle.lines:
        path = process_code(list(line), robots=25)
        print(line, ":", "".join(path), len(path))
        total += calc_score(line, path)
    return total
