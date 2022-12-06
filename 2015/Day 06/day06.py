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


@print_timing
def preprocess_input(input_text: str):
    operation = re.compile(
        "^[a-z]+ ?[a-z]+"
    )  # Find 'turn on', 'turn off', or 'toggle'.
    coords = re.compile("[0-9]+")
    instructions = [
        (operation.findall(line)[0], tuple(int(x) for x in coords.findall(line)))
        for line in input_text.split("\n")
    ]
    return instructions


@print_timing
def first(instructions) -> int:
    lights = np.zeros((1000, 1000))
    for operation, (x0, y0, x1, y1) in instructions:
        if operation == "turn on":
            lights[x0 : x1 + 1, y0 : y1 + 1] = 1
        elif operation == "turn off":
            lights[x0 : x1 + 1, y0 : y1 + 1] = 0
        elif operation == "toggle":
            lights[x0 : x1 + 1, y0 : y1 + 1] = 1 - lights[x0 : x1 + 1, y0 : y1 + 1]
    return np.sum(lights).astype(int)


@print_timing
def second(instructions) -> int:
    lights = np.zeros((1000, 1000))
    for operation, (x0, y0, x1, y1) in instructions:
        if operation == "turn on":
            lights[x0 : x1 + 1, y0 : y1 + 1] += 1
        elif operation == "turn off":
            lights[x0 : x1 + 1, y0 : y1 + 1] -= 1
            lights = np.maximum(lights, 0)
        elif operation == "toggle":
            lights[x0 : x1 + 1, y0 : y1 + 1] += 2
    return np.sum(lights).astype(int)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=6, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
