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
def preprocess_input(input_text: str):
    instructions = []
    for line in input_text.split("\n"):
        dir, n = line.split(" ")
        instructions.append((dir, int(n)))
    return instructions


def move_rope(instructions: list[tuple[str, int]], n_knots: int) -> int:

    dirs = {
        "U": np.array([0, 1]),
        "D": np.array([0, -1]),
        "L": np.array([-1, 0]),
        "R": np.array([1, 0]),
    }
    knots = [np.array([0, 0]) for _ in range(n_knots)]
    history = []

    for dir, n in instructions:
        for _ in range(n):
            for p in range(1, n_knots):
                head = knots[p - 1]
                tail = knots[p]
                if p == 1:  # For the first step, move the head as instructed
                    head += dirs[dir]

                delta = head - tail  # Calculate difference in position
                # If the (relative) tail is further than 1 unit away in any direction
                if any(np.abs(delta) > 1):
                    # Move it in any non-zero direction by one step
                    knots[p] += np.sign(delta)  # fmt: off
            history.append(tuple(knots[-1]))
    unique_places = set(history)
    return len(unique_places)


@print_timing
def first(instructions) -> int:
    return move_rope(instructions, 2)


@print_timing
def second(instructions) -> int:
    return move_rope(instructions, 10)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=9, year=2022)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
