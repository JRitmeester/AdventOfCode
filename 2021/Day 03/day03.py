import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint
import pandas as pd
from collections import Counter


def binary_array_to_int(arr):
    return int("".join([str(bit) for bit in arr]), 2)


def o2(report) -> int:
    for i, col in enumerate(report.columns):
        bits = report[col].value_counts().sort_values(ascending=False)
        bit = 1 if bits.get(1, 0) >= bits.get(0, 0) else 0

        report = report[report[col] == bit]
        if len(report) == 1:
            break
    return binary_array_to_int(report.values[0])


def co2(report) -> int:
    for i, col in enumerate(report.columns):
        bits = report[col].value_counts().sort_values(ascending=False)
        bit = 0 if bits.get(1, 0) >= bits.get(0, 0) else 1
        report = report[report[col] == bit]
        if len(report) == 1:
            break
    return binary_array_to_int(report.values[0])


def main():
    input_raw = (Path(__file__).parent / "input.txt").read_text()
    report = (
        np.array([[bit for bit in line] for line in input_raw.split("\n")]).astype(
            np.bool
        )
        * 1
    )

    # Turn it into a Pandas dataframe for easy filtering and keeping track of indices.
    report = pd.DataFrame(report, index=None, columns=[str(n) for n in range(12)])

    # Part 1
    most_common_bits = report.mode().values[0]
    gamma = binary_array_to_int(most_common_bits)
    epsilon = binary_array_to_int(1 - most_common_bits)
    print("Answer part 1:", gamma * epsilon)

    # Part 2
    print("Answer part 2:", o2(report) * co2(report))


if __name__ == "__main__":
    main()
