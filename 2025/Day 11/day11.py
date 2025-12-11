from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint
from functools import lru_cache
import networkx as nx
import matplotlib.pyplot as plt


def preprocess_input(input_text: str):
    routing = {}
    lines = input_text.splitlines()
    for line in lines:
        device = re.findall(r"\w{3}(?=:)", line)[0]
        outputs = re.findall(r"\w{3}(?!:)", line)
        routing[device] = outputs
    return routing


def first(routing: dict) -> int:
    """Find every path from "you" to "out"

    Args:
        routing (dict): Connections from device to one or more outputs, or "you" for the starting location

    Returns:
        int: number of paths from "you" to "out"
    """
    graph = nx.DiGraph()
    for from_node, to_nodes in routing.items():
        for to_node in to_nodes:
            graph.add_edge(from_node, to_node)

    all_valid_paths = list(nx.all_simple_paths(graph, "you", "out"))
    return len(all_valid_paths)


def second(routing: dict) -> int:
    """Count all paths from "svr" to "out" that pass through "fft" and "dac" (or "dac" and "fft")

    Args:
        input_data (dict): Connections from device to one or more outputs, or "you" for the starting location

    Returns:
        int: number of paths from "svr" to "out" that pass through "fft" and "dac" (or "dac" and "fft")
    """

    # Build the directed graph
    graph = nx.DiGraph()
    for from_node, to_nodes in routing.items():
        for to_node in to_nodes:
            graph.add_edge(from_node, to_node)

    # Count paths using dynamic programming with memoization
    @lru_cache(maxsize=None)
    def count_paths(source, target):
        if source == target:
            return 1
        total = 0
        for neighbor in graph.successors(source):
            total += count_paths(neighbor, target)
        return total
    
    # Sort of chainrule the routes together, because traversing the full graph is infeasible because
    # svr is very highly connected. So a -> b -> c -> d is the same as a -> d, and the number of paths
    # can be multiplied together.

    # Route 1: svr -> fft -> dac -> out
    svr_to_fft = count_paths("svr", "fft")
    fft_to_dac = count_paths("fft", "dac")
    dac_to_out = count_paths("dac", "out")
    route1_total = svr_to_fft * fft_to_dac * dac_to_out
    print(
        f"Route 1 (svr -> fft -> dac -> out): {svr_to_fft} * {fft_to_dac} * {dac_to_out} = {route1_total}"
    )

    # Route 2: svr -> dac -> fft -> out
    svr_to_dac = count_paths("svr", "dac")
    dac_to_fft = count_paths("dac", "fft")
    fft_to_out = count_paths("fft", "out")
    route2_total = svr_to_dac * dac_to_fft * fft_to_out
    print(
        f"Route 2 (svr -> dac -> fft -> out): {svr_to_dac} * {dac_to_fft} * {fft_to_out} = {route2_total}"
    )

    # What the heck, there aren't any connections from dac to fft.
    total_paths = route1_total + route2_total
    print(f"Total paths: {route1_total} + {route2_total} = {total_paths}")

    return total_paths


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=11, year=2025)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
