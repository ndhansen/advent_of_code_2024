import itertools
import time
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


def color_classes(graph: dict[str, list[str]]) -> dict[str, int]:
    colors = defaultdict(set)
    for vertex in graph:
        i = 1
        neighbors = set(graph[vertex])
        while colors[i] & neighbors:
            i += 1
        colors[i].add(vertex)

    inverted = {}
    for k, vs in colors.items():
        for v in vs:
            inverted[v] = k
    return inverted


def max_clique_2003(
    graph: dict[str, list[str]], coloring: dict[str, int]
) -> frozenset[str]:
    clique = set()
    max_clique = frozenset()
    vertexes = sorted(list(graph.keys()), key=lambda x: coloring[x])
    while vertexes:
        current = vertexes.pop()
        if len(clique) + coloring[current] >= len(max_clique):
            clique.add(current)
            intersection = set(vertexes) & set(graph[current])
            if intersection:
                new_graph = {}
                for v in intersection:
                    new_graph[v] = list(set(graph[v]) & intersection)
                new_coloring = color_classes(new_graph)
                possible_max_clique = max_clique_2003(new_graph, new_coloring) | clique
                if len(possible_max_clique) > len(max_clique):
                    max_clique = frozenset(possible_max_clique)
            else:
                if len(clique) > len(max_clique):
                    max_clique = frozenset(clique)
            clique.remove(current)
        else:
            return max_clique
    return max_clique


def part_2(puzzle: PuzzleInput) -> Any:
    network = parse(puzzle)
    start = time.time()
    res = ",".join(sorted(list(maximal_clique_polynomial(network))))
    end = time.time()
    total_time = end - start
    print(res)
    print("Time taken:", total_time)
    start = time.time()
    color = color_classes(network)
    res = ",".join(sorted(list(max_clique_2003(network, color))))
    end = time.time()
    total_time = end - start
    print(res)
    print("Time taken:", total_time)
    start = time.time()
    res = ",".join(sorted(list(max_clique_bruteforce(network))))
    end = time.time()
    total_time = end - start
    print(res)
    print("Time taken:", total_time)
    return res
