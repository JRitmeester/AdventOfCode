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
    calories = [
        sum(int(n) for n in elf.split("\n")) for elf in input_text.split("\n\n")
    ]
    return calories


@print_timing
def first(calories_per_elf: list[int]) -> int:
    return max(calories_per_elf)


@print_timing
def second(calories_per_elf: list[int]) -> int:
    return pd.Series(calories_per_elf).nlargest(3).sum()


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=1, year=2022)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
