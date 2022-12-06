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
    return input_text


@print_timing
def first(input_data) -> int:
    for i in range(4, len(input_data)):
        if len(set(input_data[i - 4 : i])) == 4:
            return i


@print_timing
def second(input_data) -> int:
    for i in range(14, len(input_data)):
        if len(set(input_data[i - 14 : i])) == 14:
            return i


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=6, year=2022)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
