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

from aoc_util.helpers import load_input_data


def preprocess_input(input_text: str):
    lanternfish_dict = {
        int(days): input_text.count(days) for days in set(input_text) if days != ","
    }
    return lanternfish_dict


def evolve(lanternfish: dict, days: int) -> dict:
    for day in range(days):
        new_lanternfish_dict = {}
        for days_left, num_fish in lanternfish.items():
            new_lanternfish_dict[days_left - 1] = num_fish
        new_lanternfish = new_lanternfish_dict.get(-1, 0)
        new_lanternfish_dict[-1] = 0
        new_lanternfish_dict[8] = new_lanternfish_dict.get(8, 0) + new_lanternfish
        new_lanternfish_dict[6] = new_lanternfish_dict.get(6, 0) + new_lanternfish
        lanternfish = new_lanternfish_dict
    return lanternfish


def first(input) -> int:
    lanternfish = evolve(input, days=80)
    return sum(lanternfish.values())


def second(input) -> int:
    lanternfish = evolve(input, days=256)
    return sum(lanternfish.values())


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=1, year=2021)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
