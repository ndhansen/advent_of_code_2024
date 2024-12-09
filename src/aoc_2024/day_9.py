from typing import Any, NamedTuple

from aoc.puzzle import PuzzleInput


class DiskFile(NamedTuple):
    start_index: int
    file_id: int
    size: int


def get_free_space(puzzle: PuzzleInput) -> list[tuple[int, int]]:
    free = []
    idx = 0
    is_file = True
    for size in puzzle.lines[0]:
        if not is_file:
            free.append((idx, int(size)))
        idx += int(size)
        is_file = not is_file
    return free


def get_sparse_disk(puzzle: PuzzleInput) -> dict[int, DiskFile]:
    disk_map = {}
    idx = 0
    filenum = 0
    is_file = True
    for size in puzzle.lines[0]:
        if is_file:
            disk_map[filenum] = DiskFile(idx, filenum, int(size))
            filenum += 1
        idx += int(size)
        is_file = not is_file
    return disk_map


def brute_force_parse(puzzle: PuzzleInput) -> list[int | None]:
    disk = []
    is_file = True
    i = 0
    for size in puzzle.lines[0]:
        if is_file:
            disk.extend([i] * int(size))
            i += 1
        else:
            disk.extend([None] * int(size))
        is_file = not is_file
    return disk


def brute_force_solve(disk: list[int | None]):
    left = 0
    right = len(disk) - 1
    while left < right:
        while disk[left] is not None:
            left += 1
        while disk[right] is None:
            right -= 1
        if left > right:
            break

        disk[left], disk[right] = disk[right], disk[left]
        left += 1
        right -= 1

    total = 0
    for idx, block in enumerate(disk):
        if block is None:
            break
        total += idx * block
    return total


def brute_force_part_2(
    disk_map: dict[int, DiskFile], free: list[tuple[int, int]]
) -> int:
    last_id = max(disk_map.keys())
    for file_id in range(last_id, -1, -1):
        cur_file = disk_map[file_id]
        for i in range(len(free)):
            if free[i][0] >= cur_file.start_index:
                break
            if free[i][1] >= cur_file.size:
                disk_map[file_id] = DiskFile(free[i][0], file_id, cur_file.size)
                remaining_space = free[i][1] - cur_file.size
                if remaining_space == 0:
                    free.pop(i)
                else:
                    free[i] = (free[i][0] + cur_file.size, remaining_space)
                break

    total = 0
    for disk_file in disk_map.values():
        for i in range(disk_file.size):
            total += disk_file.file_id * (disk_file.start_index + i)
    return total


def part_1(puzzle: PuzzleInput) -> Any:
    disk = brute_force_parse(puzzle)
    return brute_force_solve(disk)


def part_2(puzzle: PuzzleInput) -> Any:
    free_space = get_free_space(puzzle)
    disk = get_sparse_disk(puzzle)
    return brute_force_part_2(disk, free_space)
