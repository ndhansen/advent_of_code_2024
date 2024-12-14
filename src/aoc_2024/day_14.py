from typing import Any, NamedTuple

from aoc.datatypes import Coord
from aoc.puzzle import PuzzleInput
from tqdm import tqdm


class Robot(NamedTuple):
    start: Coord
    velocity: Coord


def parse(puzzle: PuzzleInput) -> list[Robot]:
    robots = []
    for line in puzzle.lines:
        p, v = line.split(" ")
        pos_str = p[2:]
        vel_str = v[2:]
        pos_col, pos_row = pos_str.split(",")
        vel_col, vel_row = vel_str.split(",")
        pos = Coord(int(pos_row), int(pos_col))
        vel = Coord(int(vel_row), int(vel_col))
        robots.append(Robot(pos, vel))
    return robots


def display(robots: list[Coord], map_size: Coord) -> None:
    for row in range(map_size.row):
        for col in range(map_size.col):
            current = Coord(row, col)
            total = 0
            for robot in robots:
                if robot == current:
                    total += 1
            if total == 0:
                print(".", end="")
            else:
                print(total, end="")
        print()


def get_safety_score(robots: list[Robot], steps: int, test: bool) -> int:
    map_size = Coord(103, 101)
    if test:
        map_size = Coord(7, 11)

    robot_pos = []
    for robot in robots:
        new_row = (robot.start.row + (robot.velocity.row * steps)) % map_size.row
        new_col = (robot.start.col + (robot.velocity.col * steps)) % map_size.col
        new_pos = Coord(new_row, new_col)
        robot_pos.append(new_pos)

    quadrants = [0, 0, 0, 0]
    for robot in robot_pos:
        if robot.row < (map_size.row // 2):
            if robot.col < (map_size.col // 2):
                quadrants[0] += 1
            elif robot.col > (map_size.col // 2):
                quadrants[1] += 1
        if robot.row > (map_size.row // 2):
            if robot.col < (map_size.col // 2):
                quadrants[2] += 1
            elif robot.col > (map_size.col // 2):
                quadrants[3] += 1

    display(robot_pos, map_size)
    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def christmas(robots: list[Robot], steps: int, test: bool) -> None:
    for i in range(1000):
        print("STEPS", i)
        get_safety_score(robots, i, test)


def christmas_2(robots: list[Robot], test: bool) -> None:
    hashes = []
    for steps in tqdm(range(10403)):
        map_size = Coord(103, 101)
        if test:
            map_size = Coord(7, 11)

        robot_pos = []
        for robot in robots:
            new_row = (robot.start.row + (robot.velocity.row * steps)) % map_size.row
            new_col = (robot.start.col + (robot.velocity.col * steps)) % map_size.col
            new_pos = Coord(new_row, new_col)
            robot_pos.append(new_pos)

        points = frozenset(robot_pos)
        if hashes and hash(points) == hashes[0]:
            print("Hit a loop I think at ", steps)
            # break
        else:
            hashes.append(hash(points))

        neighbors = 0
        for robot in robot_pos:
            for i in [
                Coord(-1, -1),
                Coord(-1, 0),
                Coord(-1, 1),
                Coord(0, -1),
                Coord(0, 1),
                Coord(1, -1),
                Coord(1, 0),
                Coord(1, 1),
            ]:
                current = robot + i
                if current in points:
                    neighbors += 1
                    break

        print(neighbors)

        if neighbors > 350:
            print("Maybe found match at", steps)
            display(robot_pos, map_size)
            return steps

    # flood_fill = 1
    # frontier = [Coord(1, 1)]
    # seen = set(frontier)
    # while frontier:
    #     current = frontier.pop()
    #     for direction in [
    #         Direction.NORTH,
    #         Direction.SOUTH,
    #         Direction.EAST,
    #         Direction.WEST,
    #     ]:
    #         neighbor = current + direction
    #         if (
    #             neighbor.col < 0
    #             or neighbor.row < 0
    #             or neighbor.row >= map_size.row
    #             or neighbor.col >= map_size.col
    #         ):
    #             continue
    #         if neighbor not in points and neighbor not in seen:
    #             flood_fill += 1
    #             frontier.append(neighbor)
    #             seen.add(neighbor)
    # print(flood_fill)
    # print("Maybe found match at", steps)
    # display(robot_pos, map_size)
    # if flood_fill in (9904, 9944, 9947, 9941, 9943):
    #     print("Maybe found match at", steps)
    #     display(robot_pos, map_size)
    # for k, v in distribution.items():
    #     print(k, ":", v)

    # neighbors = 0
    # for robot in robot_pos:
    #     for diagonal in [Coord(1, 1), Coord(-1, -1)]:
    #         if robot + diagonal in points:
    #             neighbors += 1
    #
    # if neighbors > 40:
    #     print("Maybe found match at", steps)
    #     display(robot_pos, map_size)

    # twos = 0
    # for row in range(1, 80):
    #     total = 0
    #     for col in range(0, map_size.col):
    #         current = Coord(row, col)
    #         if current in points:
    #             total += 1
    #     if total == 2:
    #         twos += 1
    #
    # if twos > 20:
    #     print("Maybe found match at", steps)
    #     display(robot_pos, map_size)

    # center_radius = 5
    # center_total = 0
    # for robot in robot_pos:
    #     if (
    #         abs((map_size.row // 2) - robot.row) < center_radius
    #         and abs((map_size.col // 2) - robot.col) < center_radius
    #     ):
    #         center_total += 1
    # if center_total > 15:
    #     print("Maybe found match at", steps)
    #     display(robot_pos, map_size)


def part_1(puzzle: PuzzleInput) -> Any:
    robots = parse(puzzle)
    return get_safety_score(robots, 100, puzzle.test)


def part_2(puzzle: PuzzleInput) -> Any:
    robots = parse(puzzle)
    return christmas_2(robots, puzzle.test)
