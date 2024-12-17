from collections import defaultdict
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
    _, target_ops = parse(puzzle)
    op_to_reg = defaultdict(list)
    reg_to_op = {}
    for i in range(1024):
        computer, ops = parse(puzzle)
        computer.a = i
        result_ops = [int(x) for x in run(computer, ops).split(",")]
        op_to_reg[result_ops[0]].append(i)
        reg_to_op[i] = result_ops[0]

    import pudb

    pudb.set_trace()
    possibles = op_to_reg[target_ops[0]]
    for i, target in enumerate(target_ops[1:], start=1):
        new_possibles = []
        # For each possible number
        for possible in possibles:
            # Cut off three bits from the end
            current = possible >> (3 * i)
            # Try out 000 through 111 on the start
            for n in range(7):
                potential = int(bin(n)[2:] + bin(current)[2:].rjust(3, "0"), base=2)
                if reg_to_op[potential] == target:
                    # Add back the bits I cut off
                    new_possibles.append(int(bin(n)[2:] + bin(possible)[2:], base=2))
                    # new_possibles.append((potential << (3)) | (possible % 8))

        if len(new_possibles) == 0:
            raise ValueError("Ran out of numbers :'(")

        possibles = new_possibles

    print(possibles)


def part_2(puzzle: PuzzleInput) -> Any:
    i = 0
    while i < 1024 * 16:
        computer, ops = parse(puzzle)
        computer.a = i
        result_ops = [int(x) for x in run(computer, ops).split(",")]
        if result_ops[:3] == [2, 4, 1] or result_ops[:3] == [4, 1, 7]:
            print(i, bin(i), result_ops)
        if result_ops == ops:
            return i
        i += 1
    # smarter_brute_force(puzzle)


"""
1: 2,4
b = a mod 8
2: 1,7
b = b ^ 7
3: 7,5
c = a / (2 ** b)
4: 0,3
a = a / (2 ** 3)
5: 1,7
b = b ^ 7
6: 4,1
b = b ^ c
7: 5,5
output b % 8
8: 3,0
jump to 1 if a isn't 0


last 3 bits have to be 010
2

250 = 5,

923 0b1110011011 [2, 4, 1, 1]
925 0b1110011101 [2, 4, 1, 1]
1796 0b11100000100 [4, 1, 7, 3]
1797 0b11100000101 [4, 1, 7, 3]
1947 0b11110011011 [2, 4, 1, 3]
1949 0b11110011101 [2, 4, 1, 3]
2761 0b101011001001 [2, 4, 1, 4]
2826 0b101100001010 [2, 4, 1, 4]
2971 0b101110011011 [2, 4, 1, 4]
2973 0b101110011101 [2, 4, 1, 4]
3995 0b111110011011 [2, 4, 1, 0]
3997 0b111110011101 [2, 4, 1, 0]
4298 0b1000011001010 [4, 1, 7, 0, 1]
4339 0b1000011110011 [4, 1, 7, 0, 1]
4851 0b1001011110011 [4, 1, 7, 1, 1]
5019 0b1001110011011 [2, 4, 1, 1, 1]
5021 0b1001110011101 [2, 4, 1, 1, 1]
6043 0b1011110011011 [2, 4, 1, 3, 1]
6045 0b1011110011101 [2, 4, 1, 3, 1]
6922 0b1101100001010 [2, 4, 1, 6, 1]
7067 0b1101110011011 [2, 4, 1, 6, 1]
7069 0b1101110011101 [2, 4, 1, 6, 1]
7827 0b1111010010011 [2, 4, 1, 0, 1]
8091 0b1111110011011 [2, 4, 1, 0, 1]
8093 0b1111110011101 [2, 4, 1, 0, 1]
9115 0b10001110011011 [2, 4, 1, 1, 2]
9117 0b10001110011101 [2, 4, 1, 1, 2]
9746 0b10011000010010 [2, 4, 1, 2, 2]
9747 0b10011000010011 [2, 4, 1, 2, 2]
9988 0b10011100000100 [4, 1, 7, 2, 2]
9989 0b10011100000101 [4, 1, 7, 2, 2]
10139 0b10011110011011 [2, 4, 1, 2, 2]
10141 0b10011110011101 [2, 4, 1, 2, 2]
10762 0b10101000001010 [2, 4, 1, 0, 2]
10953 0b10101011001001 [2, 4, 1, 0, 2]
11018 0b10101100001010 [2, 4, 1, 0, 2]
11163 0b10101110011011 [2, 4, 1, 0, 2]
11165 0b10101110011101 [2, 4, 1, 0, 2]
11794 0b10111000010010 [2, 4, 1, 0, 2]
11795 0b10111000010011 [2, 4, 1, 0, 2]
12187 0b10111110011011 [2, 4, 1, 0, 2]
12189 0b10111110011101 [2, 4, 1, 0, 2]
12290 0b11000000000010 [2, 4, 1, 0, 3]
12490 0b11000011001010 [4, 1, 7, 0, 3]
12531 0b11000011110011 [4, 1, 7, 0, 3]
12802 0b11001000000010 [2, 4, 1, 1, 3]
13043 0b11001011110011 [4, 1, 7, 1, 3]
13211 0b11001110011011 [2, 4, 1, 1, 3]
13213 0b11001110011101 [2, 4, 1, 1, 3]
13842 0b11011000010010 [2, 4, 1, 2, 3]
13843 0b11011000010011 [2, 4, 1, 2, 3]
14235 0b11011110011011 [2, 4, 1, 2, 3]
14237 0b11011110011101 [2, 4, 1, 2, 3]
14858 0b11101000001010 [2, 4, 1, 2, 3]
15114 0b11101100001010 [2, 4, 1, 2, 3]
15259 0b11101110011011 [2, 4, 1, 2, 3]
15261 0b11101110011101 [2, 4, 1, 2, 3]
15890 0b11111000010010 [2, 4, 1, 0, 3]
15891 0b11111000010011 [2, 4, 1, 0, 3]
16283 0b11111110011011 [2, 4, 1, 0, 3]
16285 0b11111110011101 [2, 4, 1, 0, 3]
"""
