import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data


def preprocess_input(input_text: str, shape=(137, 139)):
    squashed = "".join(input_text.split("\n"))
    field = np.array([n for n in squashed]).reshape(shape)
    return field


def first(field) -> int:
    step = 0
    while True:
        step += 1
        field_start = np.copy(field)

        east_cucumbers = field == ">"
        south_cucumbers = field == "v"
        all_cucumbers = np.logical_or(east_cucumbers, south_cucumbers)

        east_next_pos = np.roll(east_cucumbers, 1, axis=1)
        east_valid_move = np.logical_and(east_next_pos, ~all_cucumbers)
        east_old_pos = np.roll(east_valid_move, -1, axis=1)
        field[np.nonzero(east_valid_move)] = ">"
        field[np.nonzero(east_old_pos)] = "."

        east_cucumbers = field == ">"
        south_cucumbers = field == "v"
        all_cucumbers = np.logical_or(east_cucumbers, south_cucumbers)

        south_next_pos = np.roll(south_cucumbers, 1, axis=0)
        south_valid_move = np.logical_and(south_next_pos, ~all_cucumbers)
        south_old_pos = np.roll(south_valid_move, -1, axis=0)
        field[np.nonzero(south_valid_move)] = "v"
        field[np.nonzero(south_old_pos)] = "."
        if np.array_equal(field_start, field):
            print(f"EQUAL after {step} steps!")
            return step


def second(input) -> int:
    pass


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=25, year=2021)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
