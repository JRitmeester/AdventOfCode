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

from aoc_util.helpers import input_to_np_arr, load_input_data


def preprocess_input(input_original: str):
    input = input_original.split("\n")
    report = np.array([[bit for bit in line] for line in input]).astype(bool) * 1
    # Turn it into a Pandas dataframe for easy filtering and keeping track of indices.
    report = pd.DataFrame(
        report, index=None, columns=[str(n) for n in range(len(report[0]))]
    )
    return report


def binary_array_to_int(arr: list) -> int:
    """Turn an array of bits into the decimal number that it represent"""
    return int("".join([str(bit) for bit in arr]), 2)


def o2(report: pd.DataFrame) -> int:
    for i, col in enumerate(report.columns):
        bits = report[col].value_counts().sort_values(ascending=False)
        bit = 1 if bits.get(1, 0) >= bits.get(0, 0) else 0

        report = report[report[col] == bit]
        if len(report) == 1:
            break
    return binary_array_to_int(report.values[0])


def co2(report: pd.DataFrame) -> int:
    for i, col in enumerate(report.columns):
        bits = report[col].value_counts().sort_values(ascending=False)
        bit = 0 if bits.get(1, 0) >= bits.get(0, 0) else 1
        report = report[report[col] == bit]
        if len(report) == 1:
            break
    return binary_array_to_int(report.values[0])


def first(report: pd.DataFrame) -> int:
    most_common_bits = report.mode().values[0]
    gamma = binary_array_to_int(most_common_bits)
    epsilon = binary_array_to_int(1 - most_common_bits)
    return gamma * epsilon


def second(report: pd.DataFrame) -> int:
    return o2(report) * co2(report)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=3, year=2021)
    report = preprocess_input(original_input)
    print("The answer to part 1 is:", first(report))
    print("The answer to part 2 is:", second(report))
