import contextlib
from typing import Any

import networkx as nx
from aoc.puzzle import PuzzleInput


def get_graph(puzzle: PuzzleInput) -> nx.DiGraph:
    edges = []
    for line in puzzle.lines:
        if line.strip() == "":
            break
        left_str, right_str = line.split("|")
        left, right = int(left_str), int(right_str)
        edges.append((left, right))

    return nx.DiGraph(edges)


def get_pagesets(puzzle: PuzzleInput) -> list[list[int]]:
    rules = []
    rules_raw = puzzle.raw.split("\n\n", 1)[1]
    for rule in rules_raw.strip().split("\n"):
        current_rule = []
        for item in rule.strip().split(","):
            current_rule.append(int(item))
        rules.append(current_rule)

    return rules


def remove_other_nodes(graph: nx.DiGraph, retained_nodes: set[int]) -> nx.DiGraph:
    local_graph = graph.copy()
    other_nodes = set(local_graph.nodes.keys()) - retained_nodes
    for other_node in other_nodes:
        local_graph.remove_node(other_node)

    return local_graph


def get_correct_order(graph: nx.DiGraph, pages: list[int]) -> list[int]:
    smallgraph = remove_other_nodes(graph, set(pages))
    with contextlib.suppress(nx.NetworkXNoCycle):
        nx.algorithms.find_cycle(smallgraph)
        msg = "Cycle found, this might not work."
        raise ValueError(msg)
    path = list(nx.algorithms.topological_sort(smallgraph))
    return path


def get_valid_medians(graph: nx.DiGraph, page_sets: list[list[int]]) -> int:
    total = 0
    for pages in page_sets:
        result = get_correct_order(graph, pages)
        if result == pages:
            total += result[len(result) // 2]
    return total


def part_1(puzzle: PuzzleInput) -> Any:
    pagesets = get_pagesets(puzzle)
    graph = get_graph(puzzle)
    return get_valid_medians(graph, pagesets)


def get_all_medians(graph: nx.DiGraph, page_sets: list[list[int]]) -> int:
    total = 0
    for pages in page_sets:
        result = get_correct_order(graph, pages)
        total += result[len(result) // 2]
    return total


def part_2(puzzle: PuzzleInput) -> Any:
    pagesets = get_pagesets(puzzle)
    wrong_pagesets = []
    graph = get_graph(puzzle)
    for pages in pagesets:
        if get_correct_order(graph, pages) != pages:
            wrong_pagesets.append(pages)
    return get_all_medians(graph, wrong_pagesets)
