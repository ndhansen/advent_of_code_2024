import contextlib
from collections import defaultdict
from typing import Any

import networkx as nx
from aoc.puzzle import PuzzleInput


def get_graph(puzzle: PuzzleInput) -> dict[int, set[int]]:
    graph = defaultdict(set)
    for line in puzzle.lines:
        if line.strip() == "":
            break
        left_str, right_str = line.split("|")
        left, right = int(left_str), int(right_str)
        graph[right].add(left)
    return graph


def get_netgraph(puzzle: PuzzleInput) -> nx.DiGraph:
    edges = []
    for line in puzzle.lines:
        if line.strip() == "":
            break
        left_str, right_str = line.split("|")
        left, right = int(left_str), int(right_str)
        edges.append((left, right))

    return nx.DiGraph(edges)


def remove_other_nodes(graph: nx.DiGraph, retained_nodes: set[int]) -> nx.DiGraph:
    local_graph = graph.copy()
    other_nodes = set(local_graph.nodes.keys()) - retained_nodes
    for other_node in other_nodes:
        for in_src, _ in local_graph.in_edges(other_node):
            for _, out_dst in local_graph.out_edges(other_node):
                local_graph.add_edge(in_src, out_dst)

        local_graph.remove_node(other_node)

    to_remove = []
    for a, b in local_graph.edges():
        if a == b:
            to_remove.append(a)
    for node in to_remove:
        local_graph.remove_edge(node, node)

    return local_graph


def check_valid(graph: nx.DiGraph, page_sets: list[list[int]]) -> None:
    for pages in page_sets:
        smallgraph = remove_other_nodes(graph, set(pages))
        with contextlib.suppress(nx.NetworkXNoCycle):
            if nx.find_cycle(smallgraph):
                import pudb

                pudb.set_trace()
                msg = "Cycle found, this might not work."
                raise ValueError(msg)
        path = list(nx.algorithms.topological_sort(smallgraph))
        print(path)
        nx.drawing.nx_agraph.write_dot(
            smallgraph, path="src/aoc_2024/inputs/day_5/test.dot"
        )


def get_updates(puzzle: PuzzleInput) -> list[list[int]]:
    rules = []
    rules_raw = puzzle.raw.split("\n\n", 1)[1]
    for rule in rules_raw.strip().split("\n"):
        current_rule = []
        for item in rule.strip().split(","):
            current_rule.append(int(item))
        rules.append(current_rule)

    return rules


def process_updates(graph: dict[int, set[int]], rules: list[list[int]]) -> int:
    total = 0
    i = 0
    for rule in rules:
        result = process_update(graph, rule)
        if result:
            print(f"rule {i} passed, result: {result}")
            total += result
        i += 1
    return total


def process_update(graph: dict[int, set[int]], rule: list[int]) -> int | None:
    for current, priors in graph.items():
        if current in rule:
            current_idx = rule.index(current)
            for prior in priors:
                if prior in rule and rule.index(prior) > current_idx:
                    return None
    return rule[len(rule) // 2]


def maybe_reorder(current: int, priors: set[int], rule: list[int]) -> list[int] | None:
    if current in rule:
        current_idx = rule.index(current)
        for prior in priors:
            if prior in rule and rule.index(prior) < current_idx:
                rule = rule.copy()
                rule.remove(current)
                prior_idx = rule.index(prior)
                rule.insert(prior_idx, current)
                return rule
    return None


def process_updates_2(graph: dict[int, set[int]], rules: list[list[int]]) -> int:
    total = 0
    for rule in rules:
        total += process_update_2(graph, rule)
    return total


def process_update_2(graph: dict[int, set[int]], rule: list[int]) -> int:
    for current, priors in graph.items():
        while (new_rule := maybe_reorder(current, priors, rule)) is not None:
            rule = new_rule
    return rule[len(rule) // 2]


def part_1(puzzle: PuzzleInput) -> Any:
    netgraph = get_netgraph(puzzle)
    graph = get_graph(puzzle)
    rules = get_updates(puzzle)
    check_valid(netgraph, rules)
    return process_updates(graph, rules)


def part_2(puzzle: PuzzleInput) -> Any:
    graph = get_graph(puzzle)
    rules = get_updates(puzzle)
    # wrong_rules = []
    # for rule in rules:
    #     if process_update(graph, rule) is None:
    #         wrong_rules.append(rule)
    # return process_updates_2(graph, wrong_rules)
