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
from aoc_util.helpers import input_to_np_arr, load_input_data


def preprocess_input(input_text: str):
    return input_to_np_arr(input_text.split("\n"), dtype=int)


def first(input):
    n_increasing = np.count_nonzero(np.convolve(input, [1, -1], mode="valid") > 0)
    return n_increasing


def second(input):
    sliding_signal = np.convolve(input, [1, 1, 1], mode="valid")
    n_increasing = np.count_nonzero(
        np.convolve(sliding_signal, [1, -1], mode="valid") > 0
    )
    return n_increasing


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=1, year=2021)
    input_ = preprocess_input(original_input)
    print("The answer to part 1 is:", first(input_))
    print("The answer to part 2 is:", second(input_))
