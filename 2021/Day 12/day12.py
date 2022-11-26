import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data


def find_number_of_routes(connections, path=None) -> int:

    if not path:
        path = ["start"]
    total = 0

    # Check the cave that was added last, and explore its connections.
    for cave in connections[path[-1]]:

        # If it is a big cave, or it hasn't been explored yet,
        # check if the cave is the end. If not, explore its connectinos
        # by calling this functions again with this cave added to the path.
        if cave.isupper() or cave not in path:

            # If it's the end, just add one to the total number of routes.
            # Otherwise, keep searching.
            if cave == "end":
                total += 1
            else:
                total += find_number_of_routes(connections, path + [cave])
    return total


def find_number_of_routes2(connections, path=None):
    if not path:
        path = ["start"]
    total = 0
    for cave in connections[path[-1]]:
        if cave == "end":
            total += 1
        else:
            if cave.islower() and cave in path:
                num_routes = find_number_of_routes(connections, path + [cave])
            else:
                num_routes = find_number_of_routes2(connections, path + [cave])
            total += num_routes
    return total


def preprocess_input(input_text: str):
    connections = defaultdict(list)

    for line in input_text.split("\n"):
        pair = line.split("-")

        # Add a two-way connection between cave a and b,
        # for each connection in the input file.
        for a, b in zip(pair, reversed(pair)):
            if b != "start":
                connections[a].append(b)
    return connections


def first(input) -> int:
    return find_number_of_routes(input)


def second(input) -> int:
    return find_number_of_routes2(input)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=12, year=2021)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
