import re
import sys
from itertools import permutations
from pathlib import Path
from pprint import pprint

import numpy as np
import pandas as pd

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data, print_timing


def calculate_route_length(route, distances):
    return sum(distances[(route[i - 1], route[i])] for i in range(1, len(route)))


@print_timing
def preprocess_input(input_text: str):
    lines = input_text.split("\n")
    connection_lengths = {}
    for line in lines:
        origin, destination, distance = re.match(
            "(\w+) to (\w+) = (\d+)", line
        ).groups()
        connection_lengths[(origin, destination)] = int(distance)
        connection_lengths[(destination, origin)] = int(distance)

    cities = set([city for city, _ in connection_lengths.keys()])
    routes = set(permutations(cities))
    distances = [calculate_route_length(route, connection_lengths) for route in routes]
    return distances


@print_timing
def first(route_distances) -> int:
    return min(route_distances)


@print_timing
def second(route_distances) -> int:
    return max(route_distances)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=9, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
