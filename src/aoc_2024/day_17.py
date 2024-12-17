from typing import Any

from aoc.puzzle import PuzzleInput


class Machine:
    def __init__(self, a: int, b: int, c: int) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.output = []

    def result(self) -> str:
        return ",".join(str(x) for x in self.output)

    def reset(self, a: int) -> None:
        self.a = a
        self.b = 0
        self.c = 0
        self.output = []

    def combo(self, num: int) -> int:
        if num >= 0 and num <= 3:
            return num
        if num == 4:
            return self.a
        if num == 5:
            return self.b
        if num == 6:
            return self.c
        raise ValueError

    def adv(self, combo: int) -> None:
        value = self.combo(combo)
        result = int(self.a / (2**value))
        self.a = result

    def bst(self, combo: int) -> None:
        value = self.combo(combo)
        result = value % 8
        self.b = result

    def bdv(self, combo: int) -> None:
        value = self.combo(combo)
        result = int(self.a / (2**value))
        self.b = result

    def cdv(self, combo: int) -> None:
        value = self.combo(combo)
        result = int(self.a / (2**value))
        self.c = result

    def bxl(self, num: int) -> None:
        result = self.b ^ num
        self.b = result

    def bxc(self) -> None:
        result = self.b ^ self.c
        self.b = result

    def jnz(self, num: int) -> int | None:
        if self.a == 0:
            return None
        return num

    def out(self, combo: int) -> None:
        value = self.combo(combo) % 8
        self.output.append(value)


def parse(puzzle: PuzzleInput) -> tuple[Machine, list[int]]:
    registers = []
    for i in range(3):
        registers.append(int(puzzle.lines[i].split(": ")[1]))

    numbers = puzzle.lines[4].split(": ")[1]
    ops = [int(x) for x in numbers.split(",")]
    computer = Machine(registers[0], registers[1], registers[2])
    return computer, ops


def run(computer: Machine, ops: list[int], target: list[int] | None = None) -> str:
    pointer = 0
    while True:
        if pointer >= len(ops):
            break

        if target is not None:
            if computer.output == target:
                return computer.result()

        op, num = ops[pointer], ops[pointer + 1]

        match op:
            case 0:
                computer.adv(num)
            case 1:
                computer.bxl(num)
            case 2:
                computer.bst(num)
            case 3:
                move = computer.jnz(num)
                if move is not None:
                    pointer = move
                    continue
            case 4:
                computer.bxc()
            case 5:
                computer.out(num)
            case 6:
                computer.bdv(num)
            case 7:
                computer.cdv(num)
            case _:
                raise ValueError

        pointer += 2
    return computer.result()


def part_1(puzzle: PuzzleInput) -> Any:
    computer, ops = parse(puzzle)
    return run(computer, ops)


def smarter_brute_force(puzzle: PuzzleInput) -> int:
    computer, ops = parse(puzzle)

    possibles = {0}
    for target in reversed(ops):
        new_possibles = set()
        for possible in possibles:
            for n in range(8):
                potential = (possible * 8) + n
                computer.reset(potential)
                run(computer, ops)
                if computer.output[0] == target:
                    new_possibles.add(potential)
        possibles = new_possibles

    return sorted(list(possibles))[0]


def part_2(puzzle: PuzzleInput) -> Any:
    return smarter_brute_force(puzzle)
