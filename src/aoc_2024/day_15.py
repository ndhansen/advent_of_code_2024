import enum
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any

from aoc.datatypes import Coord, Direction
from aoc.puzzle import PuzzleInput


def parse_move(char: str) -> Direction:
    match char:
        case "v":
            return Direction.SOUTH
        case "^":
            return Direction.NORTH
        case "<":
            return Direction.WEST
        case ">":
            return Direction.EAST
    msg = "Invalid symbol"
    raise ValueError(msg)


def parse_moves(line: str) -> list[Direction]:
    orders = []
    for char in line:
        orders.append(parse_move(char))
    return orders


class MapObjects(enum.Enum):
    WALL = "#"
    BOX = "O"
    ROBOT = "@"
    FLOOR = "."


def parse_maze(maze_raw: list[str]) -> dict[Coord, MapObjects]:
    maze = {}
    for row, line in enumerate(maze_raw):
        for col, char in enumerate(line):
            current = Coord(row, col)
            match char:
                case MapObjects.WALL.value:
                    maze[current] = MapObjects.WALL
                case MapObjects.BOX.value:
                    maze[current] = MapObjects.BOX
                case MapObjects.FLOOR.value:
                    maze[current] = MapObjects.FLOOR
                case MapObjects.ROBOT.value:
                    maze[current] = MapObjects.ROBOT
    return maze


def gps_value(maze: dict[Coord, MapObjects]) -> int:
    total = 0
    for loc, item in maze.items():
        if item == MapObjects.BOX:
            total += (100 * loc.row) + loc.col
    return total


def parse_puzzle(
    puzzle: PuzzleInput,
) -> tuple[dict[Coord, MapObjects], list[Direction]]:
    maze_lines_raw, direction_lines_raw = puzzle.raw.split("\n\n")
    maze_lines = maze_lines_raw.splitlines()
    direction_line = "".join(direction_lines_raw.splitlines())

    maze = parse_maze(maze_lines)
    orders = parse_moves(direction_line)
    return maze, orders


def push_box(box: Coord, direction: Direction, maze: dict[Coord, MapObjects]) -> bool:
    next_loc = box + direction
    while next_loc in maze and maze[next_loc] == MapObjects.BOX:
        next_loc = next_loc + direction
    if maze[next_loc] == MapObjects.WALL:
        # All locked because they hit a wall
        return False

    # We have a floor
    maze[next_loc] = MapObjects.BOX
    maze[box] = MapObjects.FLOOR
    return True


def move_robot(maze: dict[Coord, MapObjects], orders: list[Direction]) -> int:
    robot = None
    for loc, item in maze.items():
        if item == MapObjects.ROBOT:
            robot = loc

    if robot is None:
        msg = "No robot start found"
        raise ValueError(msg)
    maze[robot] = MapObjects.FLOOR

    for order in orders:
        next_loc = robot + order
        if maze[next_loc] == MapObjects.WALL:
            pass
        elif maze[next_loc] == MapObjects.FLOOR:
            robot = next_loc
        elif maze[next_loc] == MapObjects.BOX:
            pushed = push_box(next_loc, order, maze)
            if pushed is True:
                robot = next_loc

    return gps_value(maze)


def part_1(puzzle: PuzzleInput) -> Any:
    maze, orders = parse_puzzle(puzzle)
    return move_robot(maze, orders)


@dataclass
class MO:
    left: Coord
    right: Coord

    @abstractmethod
    def can_push(self, direction: Direction, maze: dict[Coord, "MO"]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def push(self, direction: Direction, maze: dict[Coord, "MO"]) -> None:
        raise NotImplementedError


class Wall(MO):
    def can_push(self, direction: Direction, maze: dict[Coord, "MO"]) -> bool:
        return False

    def push(self, direction: Direction, maze: dict[Coord, "MO"]) -> None:
        msg = "Tried to push a wall."
        raise ValueError(msg)


class Box(MO):
    def can_push(self, direction: Direction, maze: dict[Coord, "MO"]) -> bool:
        if direction in (Direction.EAST, Direction.WEST):
            if direction == Direction.EAST:
                n = self.right + direction
            else:
                n = self.left + direction
            if n in maze:
                if isinstance(maze[n], Wall):
                    return False
                elif isinstance(maze[n], Box):
                    return maze[n].can_push(direction, maze)
                else:
                    raise ValueError
            return True
        else:
            ln = self.left + direction
            rn = self.right + direction

            left_pushable = right_pushable = True
            if ln in maze:
                left_pushable = maze[ln].can_push(direction, maze)
            if rn in maze:
                right_pushable = maze[rn].can_push(direction, maze)
            return left_pushable and right_pushable

    def push(self, direction: Direction, maze: dict[Coord, "MO"]) -> None:
        if direction in (Direction.EAST, Direction.WEST):
            if direction == Direction.EAST:
                n = self.right + direction
            else:
                n = self.left + direction
            if n in maze:
                maze[n].push(direction, maze)
        else:
            ln = self.left + direction
            rn = self.right + direction
            if ln in maze and rn in maze and maze[ln] == maze[rn]:
                maze[ln].push(direction, maze)
            else:
                if ln in maze:
                    maze[ln].push(direction, maze)
                if rn in maze:
                    maze[rn].push(direction, maze)
        del maze[self.left]
        del maze[self.right]
        self.left += direction
        self.right += direction
        maze[self.left] = self
        maze[self.right] = self


def parse_maze_2(maze_raw: list[str]) -> tuple[dict[Coord, MO], Coord]:
    maze: dict[Coord, MO] = {}
    robot = None
    for row, line in enumerate(maze_raw):
        col = 0
        for char in line:
            left = Coord(row, col)
            right = Coord(row, col + 1)
            match char:
                case MapObjects.WALL.value:
                    wall = Wall(left, right)
                    maze[left] = wall
                    maze[right] = wall
                case MapObjects.BOX.value:
                    box = Box(left, right)
                    maze[left] = box
                    maze[right] = box
                case MapObjects.ROBOT.value:
                    robot = left
            col += 2
    if robot is None:
        raise ValueError
    return maze, robot


def parse_puzzle_2(
    puzzle: PuzzleInput,
) -> tuple[dict[Coord, MO], Coord, list[Direction]]:
    maze_lines_raw, direction_lines_raw = puzzle.raw.split("\n\n")
    maze_lines = maze_lines_raw.splitlines()
    direction_line = "".join(direction_lines_raw.splitlines())

    maze, robot = parse_maze_2(maze_lines)
    orders = parse_moves(direction_line)
    return maze, robot, orders


def gps_value_2(maze: dict[Coord, MO]) -> int:
    mo = maze.values()
    seen = set()
    total = 0
    for item in mo:
        if item.left in seen:
            continue
        if isinstance(item, Box):
            total += (100 * item.left.row) + item.left.col
            seen.add(item.left)
    return total


def move_robot_2(maze: dict[Coord, MO], robot: Coord, orders: list[Direction]) -> int:
    for order in orders:
        next_loc = robot + order
        if next_loc in maze:
            if maze[next_loc].can_push(order, maze) is True:
                maze[next_loc].push(order, maze)
                robot = next_loc
        else:
            robot = next_loc

    return gps_value_2(maze)


def part_2(puzzle: PuzzleInput) -> Any:
    maze, robot, orders = parse_puzzle_2(puzzle)
    return move_robot_2(maze, robot, orders)
