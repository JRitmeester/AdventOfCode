import re
import sys
from pathlib import Path

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

result_scores = {"win": 6, "draw": 3, "lose": 0}
move_scores = {"X": 1, "Y": 2, "Z": 3}
combos = {
    ("A", "X"): "draw",
    ("A", "Y"): "win",
    ("A", "Z"): "lose",
    ("B", "X"): "lose",
    ("B", "Y"): "draw",
    ("B", "Z"): "win",
    ("C", "X"): "win",
    ("C", "Y"): "lose",
    ("C", "Z"): "draw",
}
response = {
    ("A", "X"): "Z",
    ("A", "Y"): "X",
    ("A", "Z"): "Y",
    ("B", "X"): "X",
    ("B", "Y"): "Y",
    ("B", "Z"): "Z",
    ("C", "X"): "Y",
    ("C", "Y"): "Z",
    ("C", "Z"): "X",
}


@print_timing
def preprocess_input(input_text: str) -> list[tuple[str, str]]:
    return [(l[0], l[2]) for l in input_text.split("\n")]


@print_timing
def first(turns: list[tuple[str, str]]) -> int:
    total = 0
    for opp, move in turns:
        total += result_scores[combos[(opp, move)]] + move_scores[move]
    return total


@print_timing
def second(turns: list[tuple[str, str]]) -> int:
    total = 0
    for opp, goal in turns:
        move = response[(opp, goal)]
        total += result_scores[combos[(opp, move)]] + move_scores[move]

    return total


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=2, year=2022)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
