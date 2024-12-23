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


def max_clique_bruteforce(graph: dict[str, list[str]]) -> frozenset[str]:
    """Brute force find a max clique"""
    network = {k: set(v) for k, v in graph.items()}
    edges = set()
    for k, vs in graph.items():
        for v in vs:
            edges.add(frozenset((k, v)))

    current_largest = frozenset()
    frontier = edges.copy()
    seen = edges.copy()
    while frontier:
        current = list(frontier.pop())
        interconnection = network[current[0]].copy()

        # If our node has fewer connections than the current max, exit early
        if len(interconnection) + 1 < len(current_largest):
            continue

        # Get all mutual connections
        for o in current[1:]:
            interconnection &= network[o]

        if len(interconnection) == 0:
            continue

        for o in interconnection:
            temp = set(current)
            temp.add(o)
            to_explore = frozenset(temp)
            if to_explore in seen:
                continue
            frontier.add(frozenset(to_explore))
            seen.add(frozenset(to_explore))
            if len(to_explore) > len(current_largest):
                current_largest = to_explore

    return current_largest


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

    # start = time.time()
    res = ",".join(sorted(list(maximal_clique_polynomial(network))))
    # end = time.time()
    # total_time = end - start
    # print(res)
    # print("Time taken:", total_time)
    # start = time.time()
    # res = ",".join(sorted(list(max_clique_bruteforce(network))))
    # end = time.time()
    # total_time = end - start
    # print(res)
    # print("Time taken:", total_time)
    return res
