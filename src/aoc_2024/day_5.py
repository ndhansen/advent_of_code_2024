from collections import defaultdict, deque
from typing import Any

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


def get_updates(puzzle: PuzzleInput) -> list[list[int]]:
    rules = []
    rules_raw = puzzle.raw.split("\n\n", 1)[1]
    for rule in rules_raw.strip().split("\n"):
        current_rule = []
        for item in rule.strip().split(","):
            current_rule.append(int(item))
        rules.append(current_rule)

    return rules


def is_path(graph: dict[int, set[int]], start: int, to: int, others: set[int]) -> bool:
    frontier = deque([start])
    while frontier:
        current = frontier.popleft()
        if current in others:
            return False
        if to in graph[current]:
            return True
        frontier.extendleft(list(graph[current]))
    return False


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
                    print(f"node {prior} can't come after {current} in the rule {rule}")
                    return None
    return rule[len(rule) // 2]


def maybe_reorder(current: int, priors: set[int], rule: list[int]) -> list[int] | None:
    if current in rule:
        current_idx = rule.index(current)
        for prior in priors:
            if prior in rule and rule.index(prior) < current_idx:
                print(
                    f"node {prior} can't come after {current} in the rule {rule}, reordering"
                )
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
    graph = get_graph(puzzle)
    # netgraphlist = {x: list(y) for x, y in graph.items()}
    # netgraph = nx.from_dict_of_lists(netgraphlist).to_directed()
    # print(nx.find_cycle(netgraph))
    # A = nx.nx_agraph.to_agraph(netgraph)
    # A.write("test.dot")
    rules = get_updates(puzzle)
    return process_updates(graph, rules)


def part_2(puzzle: PuzzleInput) -> Any:
    graph = get_graph(puzzle)
    rules = get_updates(puzzle)
    wrong_rules = []
    for rule in rules:
        if process_update(graph, rule) is None:
            wrong_rules.append(rule)
    return process_updates_2(graph, wrong_rules)
