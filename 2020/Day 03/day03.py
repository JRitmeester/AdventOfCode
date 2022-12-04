import sys
from pathlib import Path

import matplotlib.pyplot as plt
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


@print_timing
def preprocess_input(input_text: str, map_size: tuple = (323, 31)):
    map_oneline = np.array([char for char in "".join(input_text.split("\n"))])
    map = map_oneline.reshape(map_size) == "#"
    return map


def wheeeeeeee(map, dx, dy) -> int:
    x = 0
    y = 0
    trees = 0
    while True:
        if map.T[x][y] == True:
            trees += 1

        y += dy
        x = (x + dx) % map.shape[1]
        if y >= map.shape[0]:
            break

    return trees


@print_timing
def first(map) -> int:
    return wheeeeeeee(map, dx=3, dy=1)


@print_timing
def second(map) -> int:
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    return np.prod([wheeeeeeee(map, dx, dy) for dx, dy in slopes])


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=3, year=2020)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
