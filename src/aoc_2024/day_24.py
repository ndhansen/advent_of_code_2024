from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any, Literal

from aoc.puzzle import PuzzleInput


@dataclass
class Signal:
    gatename: str
    position: bool = False
    ready: bool = False


@dataclass
class Gate:
    in_1: Signal
    in_2: Signal
    out: Signal
    op: Literal["AND", "OR", "XOR"]

    def compute_output(self) -> None:
        match self.op:
            case "AND":
                self.out.position = self.in_1.position and self.in_2.position
            case "OR":
                self.out.position = self.in_1.position or self.in_2.position
            case "XOR":
                self.out.position = self.in_1.position != self.in_2.position


def score(gatemap: dict[str, list[Gate]]) -> int:
    zsignals = []
    for gates in gatemap.values():
        for gate in gates:
            output_name = gate.out.gatename
            if output_name.startswith("z"):
                zsignals.append((gate.out.gatename, gate.out.position))
    zsignals = list(set(zsignals))
    zsignals.sort(key=lambda x: x[0])

    solution_bits = ""
    for _, z in zsignals:
        solution_bits = str(int(z)) + solution_bits
    return int(solution_bits, base=2)


def simulate(
    inputs: dict[str, bool], gates: list[Gate], gatemap: dict[str, list[Gate]]
) -> int:
    frontier = deque(list(inputs.keys()))
    while frontier:
        current = frontier.popleft()
        for gate in gatemap[current]:
            if current == gate.in_1.gatename:
                gate.in_1.ready = True
                gate.in_1.position = inputs[current]
            if current == gate.in_2.gatename:
                gate.in_2.ready = True
                gate.in_2.position = inputs[current]

            if gate.in_1.ready and gate.in_2.ready:
                gate.compute_output()
                if not gate.out.gatename.startswith("z"):
                    frontier.append(gate.out.gatename)
                    if gate.out.position in inputs:
                        msg = "I think there's a cycle"
                        raise ValueError(msg)
                    inputs[gate.out.gatename] = gate.out.position

    return score(gatemap)


def parse(
    puzzle: PuzzleInput,
) -> tuple[dict[str, bool], list[Gate], dict[str, list[Gate]]]:
    top, bot = puzzle.raw.split("\n\n")
    inputs = {}
    for line in top.splitlines():
        sym, bit = line.split(": ", 1)
        inputs[sym] = bool(int(bit))

    gates = []
    gatemap = defaultdict(list)
    for line in bot.splitlines():
        left, op, right, _, out = line.split()

        if op not in {"AND", "OR", "XOR"}:
            raise ValueError

        l = Signal(left)
        r = Signal(right)
        o = Signal(out)
        gate = Gate(l, r, o, op)
        gatemap[left].append(gate)
        gatemap[right].append(gate)
        gates.append(gate)

    return inputs, gates, gatemap


def part_1(puzzle: PuzzleInput) -> Any:
    inputs, gates, gatemap = parse(puzzle)
    return simulate(inputs, gates, gatemap)


def swap_by_output(a: str, b: str, gates: list[Gate]) -> None:
    a_gate = None
    b_gate = None
    for gate in gates:
        if gate.out.gatename == a:
            a_gate = gate
        elif gate.out.gatename == b:
            b_gate = gate
    if a_gate is None or b_gate is None:
        raise ValueError

    a_gate.out, b_gate.out = b_gate.out, a_gate.out


def part_2(puzzle: PuzzleInput) -> Any:
    _, gates, gatemap = parse(puzzle)
    carry = None
    for gate in gatemap["x00"]:
        if gate.op == "AND":
            carry = gate
    if carry is None:
        raise ValueError

    fullmap = {}
    for gate in gates:
        inputs = (frozenset((gate.in_1.gatename, gate.in_2.gatename)), gate.op)
        fullmap[inputs] = gate

    for i in range(1, 45):
        x = "x" + str(i).rjust(2, "0")
        y = "y" + str(i).rjust(2, "0")
        z = "z" + str(i).rjust(2, "0")
        # We should find an and gate and an xor gate

    # I solved this one semi-manually
    return "gsd,kth,qnf,tbt,vpm,z12,z26,z32"
