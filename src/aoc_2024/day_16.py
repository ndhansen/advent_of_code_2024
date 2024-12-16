import heapq
import itertools
import math
from collections import defaultdict, deque
from collections.abc import Iterator, Mapping
from typing import Any, NamedTuple, Protocol

from aoc.datatypes import Coord, Direction
from aoc.exceptions import UnsolveableError
from aoc.puzzle import PuzzleInput


class Heuristic[T](Protocol):
    def __call__(self, current: T, goal: T) -> float: ...


class Cost[T](Protocol):
    def __call__(self, paths: Mapping[T, T], current: T, last: T) -> float: ...


class Neighbors[T](Protocol):
    def __call__(self, current: T, paths: Mapping[T, T]) -> Iterator[T]: ...


def _reconstruct_path[T](paths: Mapping[T, T], start: T, goal: T) -> list[T]:
    path = [goal]
    current = goal
    while current in paths:
        path.insert(0, paths[current])
        current = paths[current]
        if current == start:
            break
    return path


def a_star[T](
    start: T,
    goal: T,
    heuristic: Heuristic[T],
    cost_func: Cost[T],
    next_func: Neighbors[T],
) -> tuple[list[T], float]:
    frontier: list[tuple[float, T]] = []
    heapq.heappush(frontier, (heuristic(start, goal), start))
    paths: dict[T, T] = {}
    cheapest_path: dict[T, float] = defaultdict(lambda: float("inf"))
    cheapest_path[start] = 0.0

    while len(frontier) > 0:
        _, current = heapq.heappop(frontier)
        if current == goal:
            path = _reconstruct_path(paths, start, goal)
            return path, cheapest_path[current]

        for neighbor in next_func(current, paths):
            new_cost = cheapest_path[current] + cost_func(paths, neighbor, current)

            if new_cost < cheapest_path[neighbor]:
                paths[neighbor] = current
                cheapest_path[neighbor] = new_cost
                heapq.heappush(
                    frontier,
                    (new_cost + heuristic(neighbor, goal), neighbor),
                )

    msg = "Could not find a path."
    raise UnsolveableError(msg)


class ReindeerHeuristic(Heuristic[Coord]):
    def __call__(self, current: Coord, goal: Coord) -> float:
        return abs(current.row - goal.row) + abs(current.col - goal.col)


class ReindeerNeighbors(Neighbors[Coord]):
    def __init__(self, maze: set[Coord]) -> None:
        self.maze = maze

    def __call__(self, current: Coord, paths: Mapping[Coord, Coord]) -> Iterator[Coord]:
        for direction in (
            Direction.NORTH,
            Direction.SOUTH,
            Direction.EAST,
            Direction.WEST,
        ):
            neighbor = current + direction
            if neighbor in self.maze:
                continue
            if neighbor in paths:
                continue
            yield neighbor


class ReindeerCost(Cost[Coord]):
    def __call__(
        self, paths: Mapping[Coord, Coord], current: Coord, last: Coord
    ) -> float:
        new_facing = current - last
        prior = paths.get(last, last - Coord(0, 1))

        facing = None
        if prior is None:
            facing = Coord(0, 1)
        else:
            facing = last - prior

        if new_facing == facing:
            return 1.0
        return 1001.0


def parse(puzzle: PuzzleInput) -> tuple[set[Coord], Coord, Coord]:
    r = None
    end = None
    walls = set()
    for row, line in enumerate(puzzle.lines):
        for col, char in enumerate(line):
            current = Coord(row, col)
            match char:
                case "S":
                    r = current
                case "E":
                    end = current
                case "#":
                    walls.add(current)
    if r is None or end is None:
        raise ValueError

    return walls, r, end


def part_1(puzzle: PuzzleInput) -> Any:
    maze, start, end = parse(puzzle)
    rh = ReindeerHeuristic()
    rc = ReindeerCost()
    rn = ReindeerNeighbors(maze)
    _, cost = a_star(start, end, rh, rc, rn)
    return int(cost)


# def find_all_fastest(maze: set[Coord], start: Coord, end: Coord) -> int:
#     rh = ReindeerHeuristic()
#     rc = ReindeerCost()
#     rn = ReindeerNeighbors(maze)
#     path, cost = a_star(start, end, rh, rc, rn)
#     seen = set(path)
#     to_check = set(path[1:-1])
#     # for i in tqdm(range(1, len(path) - 1)):
#     checked = set()
#     while to_check:
#         current = to_check.pop()
#         if current == Coord(11, 4):
#             print("Got it.")
#         checked.add(current)
#         new_maze = maze.copy()
#         new_maze.add(current)
#         rn = ReindeerNeighbors(new_maze)
#         try:
#             new_path, new_cost = a_star(start, end, rh, rc, rn)
#         except UnsolveableError:
#             continue
#
#         if new_cost != cost:
#             continue
#
#         diff = set(new_path) - checked
#         to_check.update(diff)
#         seen.update(new_path)
#
#     print(seen)
#     for row in range(15):
#         for col in range(15):
#             current = Coord(row, col)
#             if current in maze:
#                 print("#", end="")
#             elif current in seen:
#                 print("O", end="")
#             else:
#                 print(".", end="")
#         print()
#     return len(seen)


class _SearchPath[S](NamedTuple):
    path: list[S]
    cost: int

    @property
    def current(self) -> S:
        return self.path[-1]


def breadth_first_search(
    *,
    start: Coord,
    goal: Coord,
    next_func: Neighbors,
    max_depth: int,
    max_cost: int,
) -> list[tuple[list[Coord], int]]:
    start_path = _SearchPath([start], 0)
    frontier = deque([start_path])
    # seen = set()
    solutions = []
    greatest_depth = 0
    while frontier:
        current_path = frontier.popleft()
        if current_path.cost > greatest_depth:
            greatest_depth = current_path.cost
            print(greatest_depth)

        if len(current_path.path) > max_depth:
            continue
        if current_path.current == goal:
            solutions.append((current_path.path, current_path.cost))
            continue
        # if current_path.current in seen:
        #     continue
        # seen.add(current_path.current)

        for next_node in next_func(
            current_path.current,
            # paths={t: s for s, t in itertools.pairwise(current_path.path)},
            paths=frozenset(current_path.path),
            # paths={},
        ):
            frontier.append(
                _SearchPath(
                    [*current_path.path, next_node],
                    current_path.cost + 1,
                ),
            )

        if len(frontier) > 10000:
            print("Culling at length:", len(frontier))
            # Culling
            for i in range(len(frontier)):
                if get_cost(frontier[i].path) > max_cost:
                    frontier.remove(frontier[i])

    return solutions


def get_cost(path: list[Coord]) -> int:
    direction = Coord(0, 1)
    cost = 0
    for a, b in itertools.pairwise(path):
        new_direction = b - a
        if new_direction != direction:
            cost += 1001
        else:
            cost += 1
        direction = new_direction
    return cost


def part_2s(puzzle: PuzzleInput) -> Any:
    maze, start, end = parse(puzzle)
    rh = ReindeerHeuristic()
    rc = ReindeerCost()
    rn = ReindeerNeighbors(maze)
    path, expected_cost = a_star(start, end, rh, rc, rn)
    sols = breadth_first_search(
        start=start,
        goal=end,
        next_func=rn,
        max_depth=len(path) + 1,
        max_cost=int(expected_cost),
    )
    all_fields = set()
    for sol_path, _ in sols:
        if get_cost(sol_path) != expected_cost:
            continue
        all_fields.update(set(sol_path))
    return len(all_fields)


def get_elbows(path: list[Coord]) -> set[Coord]:
    elbows = set()
    for i in range(len(path) - 2):
        a, b, c = path[i], path[i + 1], path[i + 2]
        if b - a != c - b:
            elbows.add(b)
    return elbows


def find_all_fastest(maze: set[Coord], start: Coord, end: Coord) -> int:
    rh = ReindeerHeuristic()
    rc = ReindeerCost()
    rn = ReindeerNeighbors(maze)
    path, expected_cost = a_star(start, end, rh, rc, rn)
    seen = set(path)
    elbows = get_elbows(path)
    impossibles = set()
    i = 1
    while True:
        success = []
        new_elbows = set()
        for combination in itertools.combinations(elbows, i):
            skip = False
            for impossible in impossibles:
                if impossible.issubset(set(combination)):
                    success.append(False)
                    skip = True
            if skip is True:
                continue

            new_maze = maze.copy()
            for combo in combination:
                new_maze.add(combo)

            rn = ReindeerNeighbors(new_maze)
            try:
                print("Trying: ", combination)
                path, cost = a_star(start, end, rh, rc, rn)
            except UnsolveableError:
                success.append(False)
                impossibles.add(frozenset(combination))
                continue

            if cost != expected_cost:
                success.append(False)
                impossibles.add(frozenset(combination))
                continue

            new_elbows.update(get_elbows(path))
            seen.update(set(path))
            success.append(True)

        if not any(success):
            break

        if elbows == elbows.union(new_elbows):
            i += 1
        else:
            elbows.update(new_elbows)

    for row in range(15):
        for col in range(15):
            current = Coord(row, col)
            if current in maze:
                print("#", end="")
            elif current in seen:
                print("O", end="")
            else:
                print(".", end="")
        print()
    return len(seen)


def part_2ss(puzzle: PuzzleInput) -> Any:
    maze, start, end = parse(puzzle)
    return find_all_fastest(maze, start, end)


def bfs(maze: set[Coord], start: Coord, end: Coord, target_cost: int) -> int:
    iterations = [(start, [], Direction.EAST, 0)]
    fastest: dict[tuple[Coord, Direction], float] = defaultdict(lambda: math.inf)
    done = False
    paths = []
    while not done:
        next_iteration = []
        for current, path, dir, cost in iterations:
            if cost > fastest[(current, dir)]:
                continue

            if current == end:
                if cost == target_cost:
                    done = True
                    paths.append([*path, current])
                else:
                    continue

            possibles = []
            if current + dir not in maze:
                possibles.append((current + dir, [*path, current], dir, cost + 1))

            if dir in (Direction.EAST, Direction.WEST):
                possibles.append((current, path, Direction.NORTH, cost + 1000))
                possibles.append((current, path, Direction.SOUTH, cost + 1000))
            else:
                possibles.append((current, path, Direction.EAST, cost + 1000))
                possibles.append((current, path, Direction.WEST, cost + 1000))

            for p in possibles:
                if fastest[(p[0], p[2])] >= p[3]:
                    fastest[(p[0], p[2])] = p[3]
                    next_iteration.append(p)

        iterations = next_iteration

    all_paths = set()
    for path in paths:
        all_paths.update(set(path))
    for row in range(15):
        for col in range(15):
            current = Coord(row, col)
            if current in maze:
                print("#", end="")
            elif current in all_paths:
                print("O", end="")
            else:
                print(".", end="")
        print()
    return len(all_paths)


def part_2(puzzle: PuzzleInput) -> Any:
    maze, start, end = parse(puzzle)
    rh = ReindeerHeuristic()
    rc = ReindeerCost()
    rn = ReindeerNeighbors(maze)
    path, cost = a_star(start, end, rh, rc, rn)
    return bfs(maze, start, end, int(cost))
