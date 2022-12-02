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
def preprocess_input(input_text: str) -> list[tuple[int, int, int]]:
    measurements = [
        tuple(int(n) for n in list(re.findall("[0-9]+", present)))
        for present in input_text.split("\n")
    ]
    return measurements


@print_timing
def first(measurements: list[tuple[int, int, int]]) -> int:
    total_surface = 0
    for w, h, l in measurements:
        a = w * h
        b = h * l
        c = w * l
        slack = min([a, b, c])
        total_surface += 2 * a + 2 * b + 2 * c + slack
    return total_surface


@print_timing
def second(measurements: list[tuple[int, int, int]]) -> int:
    total_length = 0
    for w, h, l in measurements:
        perimeter = sum(sorted([w, h, l])[0:2]) * 2
        bow = w * h * l
        total_length += perimeter + bow
    return total_length


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=2, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
