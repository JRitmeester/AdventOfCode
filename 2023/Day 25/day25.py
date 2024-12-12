from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import connected_components
import itertools
from tqdm import tqdm


def preprocess_input(input_text: str):
    connections = {}
    for line in input_text.splitlines():
        from_node, to_nodes = line.split(": ")
        to_nodes = to_nodes.split(" ")
        if from_node not in connections:
            connections[from_node] = []
        connections[from_node].extend(to_nodes)
    return connections


def first(input_data) -> int:
    graph = nx.Graph()
    for from_node, to_nodes in input_data.items():
        for to_node in to_nodes:
            graph.add_edge(from_node, to_node)
    # graph = graph.to_directed()

    # Visualize the graph

    nx.draw_spring(graph, with_labels=True)
    plt.show()

    # # Inspect which edges to cut

    graph.remove_edge("qnd", "mbk")
    graph.remove_edge("pcs", "rrl")
    graph.remove_edge("lcm", "ddl")

    # Check if the graphs are disconnected
    nx.draw_spring(graph, with_labels=True)
    plt.show()

    subgraphs = [graph.subgraph(c) for c in connected_components(graph)]
    return np.prod([len(subgraph.nodes()) for subgraph in subgraphs])


def second(input_data) -> int:
    pass


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=25, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
