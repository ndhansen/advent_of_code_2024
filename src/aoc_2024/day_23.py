import itertools
from collections import defaultdict
from typing import Any

from aoc.puzzle import PuzzleInput


def parse(puzzle: PuzzleInput) -> dict[str, list[str]]:
    network = defaultdict(list)
    for line in puzzle.lines:
        a, b = line.split("-")
        network[a].append(b)
        network[b].append(a)
    return network


def part_1(puzzle: PuzzleInput) -> Any:
    network = parse(puzzle)
    lan = set()
    for a, others in network.items():
        if a.startswith("t"):
            for b, c in itertools.combinations(others, 2):
                if b in network[c] and c in network[b]:
                    lan.add(frozenset([a, b, c]))
    return len(lan)


def maximal_clique_polynomial(graph: dict[str, list[str]]) -> frozenset[str]:
    """Faster brute force maximal clique"""
    largest_mc = frozenset()
    for vertex in graph:
        current_mc = {vertex}
        for neighbor in graph[vertex]:
            connected = True
            for mcs in current_mc:
                if mcs not in graph[neighbor]:
                    connected = False
            if connected is True:
                current_mc.add(neighbor)
        if len(current_mc) > len(largest_mc):
            largest_mc = frozenset(current_mc)
    return largest_mc


def part_2(puzzle: PuzzleInput) -> Any:
    network = parse(puzzle)

    return ",".join(sorted(list(maximal_clique_polynomial(network))))
