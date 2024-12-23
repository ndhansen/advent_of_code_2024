import itertools
from collections import defaultdict
from typing import Any

import networkx as nx
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
    print(lan)
    return len(lan)


def part_2(puzzle: PuzzleInput) -> Any:
    network = parse(puzzle)
    graph = nx.from_dict_of_lists(network)
    clique, _ = nx.algorithms.clique.max_weight_clique(graph, weight=None)
    print(clique)
    return ",".join(sorted(clique))
