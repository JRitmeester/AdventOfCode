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


def get_seat_id(instruction: str):
    step_size = 64
    row_pos = 127
    for char in [x for x in instruction][:7]:
        if char == "F":
            row_pos -= step_size
        step_size //= 2

    step_size = 4
    chair_pos = 7
    for char in [x for x in instruction][7:]:
        if char == "L":
            chair_pos -= step_size
        step_size //= 2
    return row_pos * 8 + chair_pos


@print_timing
def preprocess_input(input_text: str):
    return [get_seat_id(instruction) for instruction in input_text.split("\n")]


@print_timing
def first(seat_ids) -> int:
    return max(seat_ids)


@print_timing
def second(seat_ids) -> int:
    all_ids = list(range(128 * 7))
    for id in all_ids:
        if id in seat_ids:
            continue
        elif (id - 1) in seat_ids and (id + 1) in seat_ids:
            return id


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=5, year=2020)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
