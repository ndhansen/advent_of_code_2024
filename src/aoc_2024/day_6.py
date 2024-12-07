import enum
from typing import Any

from aoc.datatypes import Coord, Direction
from aoc.puzzle import PuzzleInput
from tqdm import tqdm


class Tile(enum.Enum):
    WALL = "#"
    FLOOR = "."


def parse_maze(puzzle: PuzzleInput) -> tuple[dict[Coord, Tile], Coord]:
    puzzzle_map = {}
    guard = None
    for row, line in enumerate(puzzle.lines):
        for col, field in enumerate(line):
            match field:
                case "^":
                    guard = Coord(row, col)
                    puzzzle_map[Coord(row, col)] = Tile.FLOOR
                case ".":
                    puzzzle_map[Coord(row, col)] = Tile.FLOOR
                case "#":
                    puzzzle_map[Coord(row, col)] = Tile.WALL
                case _:
                    msg = "Unknown tile."
                    raise ValueError(msg)

    if guard is None:
        msg = "No guard position found."
        raise ValueError(msg)
    return puzzzle_map, guard


def simulate_walk(
    puzzle: PuzzleInput, puzzle_map: dict[Coord, Tile], guard: tuple[Coord, Direction]
) -> int:
    overlapped = False
    path = set()
    path.add(guard)
    while not overlapped:
        overlapped, guard = take_step(puzzle, puzzle_map, guard, path)
    unique_positions = {pos for pos, _ in path}
    for row in range(len(puzzle.lines)):
        for col in range(len(puzzle.lines[0])):
            if Coord(row, col) in unique_positions:
                print("X", end="")
            else:
                print(puzzle_map[Coord(row, col)].value, end="")
        print()
    return len(unique_positions)


def turn(current_direction: Direction) -> Direction:
    match current_direction:
        case Direction.NORTH:
            return Direction.EAST
        case Direction.EAST:
            return Direction.SOUTH
        case Direction.SOUTH:
            return Direction.WEST
        case Direction.WEST:
            return Direction.NORTH


def out_of_bounds(pos: Coord, puzzle: PuzzleInput) -> bool:
    if pos.row < 0 or pos.col < 0:
        return True
    if pos.row >= len(puzzle.lines) or pos.col >= len(puzzle.lines[0]):
        return True
    return False


def take_step(
    puzzle: PuzzleInput,
    puzzle_map: dict[Coord, Tile],
    guard: tuple[Coord, Direction],
    path: set[tuple[Coord, Direction]],
) -> tuple[bool, tuple[Coord, Direction]]:
    new_guard_pos = guard[0] + guard[1]
    if out_of_bounds(new_guard_pos, puzzle):
        return True, (new_guard_pos, guard[1])

    # Check if we need to turn
    if puzzle_map[new_guard_pos] == Tile.WALL:
        new_guard_pos = guard[0]
        guard_direction = turn(guard[1])
    else:
        guard_direction = guard[1]

    if (new_guard_pos, guard_direction) in path:
        return True, (new_guard_pos, guard_direction)

    path.add((new_guard_pos, guard_direction))
    return False, (new_guard_pos, guard_direction)


def part_1(puzzle: PuzzleInput) -> Any:
    puzzle_map, guard = parse_maze(puzzle)
    starting_direction = Direction.NORTH
    return simulate_walk(puzzle, puzzle_map, (guard, starting_direction))


def find_loop(
    puzzle: PuzzleInput, puzzle_map: dict[Coord, Tile], guard: tuple[Coord, Direction]
) -> tuple[bool, set[Coord]]:
    done = False
    path = set()
    path.add(guard)
    while not done:
        done, guard = take_step(puzzle, puzzle_map, guard, path)
    unique_positions = {pos for pos, _ in path}
    if out_of_bounds(guard[0], puzzle):
        return False, unique_positions
    return True, unique_positions


def find_obsticle_pos(
    puzzle: PuzzleInput, puzzle_map: dict[Coord, Tile], guard: tuple[Coord, Direction]
) -> int:
    _, possible_positions = find_loop(puzzle, puzzle_map, guard)
    possible_positions.remove(guard[0])  # Remove guard starting position
    total = 0
    for current in tqdm(possible_positions):
        if puzzle_map[current] == Tile.WALL:
            msg = "Somehow we had a wall in our path"
            raise ValueError(msg)

        temp_puzzle_map = puzzle_map.copy()
        temp_puzzle_map[current] = Tile.WALL
        loop, _ = find_loop(puzzle, temp_puzzle_map, guard)
        if loop:
            total += 1
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    puzzle_map, guard = parse_maze(puzzle)
    starting_direction = Direction.NORTH
    return find_obsticle_pos(puzzle, puzzle_map, (guard, starting_direction))
