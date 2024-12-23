from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt


def find_triangles(graph: dict[str, list[str]]) -> int:
    triangles = []

    for a in graph:
        for b in graph[a]:
            # Intersection of sets finds common neighbors of a and b
            if a[0] != "t" and b[0] != "t":
                continue
            common_neighbors = graph[a].intersection(graph[b])
            for c in common_neighbors:
                if (
                    c != a and c != b
                ):  # Ensure it's a true triangle without repeated nodes
                    triangles.append((a, b, c))
    return triangles


def create_graph(connections: list[tuple[str, str]]) -> dict[str, list[str]]:
    graph = {}
    for a, b in connections:
        if a not in graph:
            graph[a] = set()
        if b not in graph:
            graph[b] = set()
        graph[a].add(b)
        graph[b].add(a)
    return graph


def preprocess_input(input_text: str) -> list[tuple[str, str]]:
    connections = []
    lines = input_text.split("\n")
    for line in lines:
        connections.append(tuple(line.split("-")))
    return connections


def first(connections: list[tuple[str, str]]) -> int:
    graph = create_graph(connections)
    triangles = find_triangles(graph)
    unique_triangles = set(tuple(sorted(triangle)) for triangle in triangles)
    return len(unique_triangles)


def second(connections: list[tuple[str, str]]) -> int:
    g = nx.Graph(connections)
    largest_group = max(nx.find_cliques(g), key=len)
    print(",".join(sorted(largest_group)))
    return len(largest_group)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=23, year=2024)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
