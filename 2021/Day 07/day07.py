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


def get_nth_triangle_number(n: int) -> int:
    """
    Triangle numbers are for summing what factorials are for multiplication.
    """
    return (n * n + n) / 2


def preprocess_input(original_input) -> np.ndarray:
    positions = np.array([int(x) for x in original_input.split(",")])
    return positions


def first(input) -> int:
    fuel_usages = np.sum([np.abs(input - x) for x in range(max(input))], axis=1)
    minimal_fuel_usage = np.min(fuel_usages)
    return minimal_fuel_usage


def second(input) -> int:
    fuel_usages = np.sum(
        [get_nth_triangle_number(np.abs(input - x)) for x in range(max(input))],
        axis=1,
    )
    minimal_fuel_usage = int(np.min(fuel_usages))
    return minimal_fuel_usage


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=8, year=2021)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
