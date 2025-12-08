from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint


def preprocess_input_one(input_text: str):
    worksheet = np.array(
        [re.findall(r"[0-9*+-]+", line) for line in input_text.splitlines()],
        dtype=object,
    )
    for i, row in enumerate(worksheet):
        if i == worksheet.shape[0] - 1:
            continue
        for j, entry in enumerate(row):
            worksheet[i][j] = int(entry)

    return worksheet


def preprocess_input_two(input_text: str):
    grid = [list(line) for line in input_text.splitlines()]
    # Pad all rows to the same length (max length)
    max_len = max(len(row) for row in grid)
    grid = [row + [" "] * (max_len - len(row)) for row in grid]
    rot_grid = np.rot90(np.array(grid))

    return rot_grid


def multiply(factors: list[int]) -> int:
    return np.prod(factors)


def add(terms: list[int]) -> int:
    return sum(terms)


def subtract(terms: list[int]) -> int:
    return terms[0] - sum(terms[1:])


OPERATOR = {"*": multiply, "+": add, "-": subtract}


def first(worksheet: np.ndarray) -> int:
    grand_total = 0
    for *entries, operator in worksheet.T:
        grand_total += OPERATOR[operator](entries)
    return grand_total


def second(rotated_worksheet: np.ndarray) -> int:
    entries = []
    grand_total = 0
    for line in rotated_worksheet:
        concat = "".join([char for char in line if char not in ["+", "-", "*"]]).strip()
        if concat.strip() == "":
            entries = []
            continue
        else:
            entries.append(int(concat))
        if "+" in line:
            grand_total += sum(entries)
        elif "-" in line:
            grand_total += subtract(entries)
        elif "*" in line:
            grand_total += multiply(entries)
    return grand_total


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=6, year=2025)
    preprocessed_input_one = preprocess_input_one(original_input)
    preprocessed_input_two = preprocess_input_two(original_input)
    print("The answer to part 1 is:", first(preprocessed_input_one))
    print("The answer to part 2 is:", second(preprocessed_input_two))
