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


def get_priority(char: str) -> int:
    return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(char) + 1


@print_timing
def preprocess_input(input_text: str):
    rucksacks = input_text.split("\n")
    return rucksacks


@print_timing
def first(rucksacks: list[str]) -> int:
    total_priority = 0
    for rucksack in rucksacks:
        half = len(rucksack) // 2
        common_item_type = next(
            iter(set(rucksack[:half]).intersection(set(rucksack[half:])))
        )
        total_priority += get_priority(common_item_type)
    return total_priority


@print_timing
def second(input_data) -> int:
    total_priority = 0
    for i in range(0, len(input_data), 3):
        group = input_data[i : i + 3]
        badge_char = next(
            iter(set(group[0]).intersection(set(group[1])).intersection(set(group[2])))
        )
        total_priority += get_priority(badge_char)
    return total_priority


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=3, year=2022)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
