import sys
from pathlib import Path

import numpy as np

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
    return np.array([n for n in input_text.split("\n")]).astype(int)


@print_timing
def first(input_data) -> int:
    for n in input_data:
        if (2020 - n) in input_data:
            return n * (2020 - n)


@print_timing
def second(input_data) -> int:
    for n in input_data:
        remainder = 2020 - n
        for m in input_data:
            if (remainder - m) in input_data:
                return (remainder - m) * n * m


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=1, year=2020)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
