from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np


def count_x_mas(grid: np.ndarray) -> int:
    rows, cols = grid.shape
    count = 0

    # Iterate through all possible centers of an "X"
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Check if the center is "A"
            if grid[r, c] != "A":
                continue

            # Validate the diagonals
            upper_left, lower_right = grid[r - 1, c - 1], grid[r + 1, c + 1]
            upper_right, lower_left = grid[r - 1, c + 1], grid[r + 1, c - 1]

            # Check diagonal from NW to SE (MAS or SAM)
            if (upper_left == "M" and lower_right == "S") or (
                upper_left == "S" and lower_right == "M"
            ):
                # Check diagonal from NE to SW (MAS or SAM)
                if (upper_right == "M" and lower_left == "S") or (
                    upper_right == "S" and lower_left == "M"
                ):
                    count += 1

    return count


def count_xmas(grid: np.ndarray) -> int:
    rows, cols = grid.shape
    count = 0

    # Horizontal and reversed horizontal
    for r in range(rows):
        for c in range(cols - 3):
            word = "".join(grid[r, c : c + 4])
            if word == "XMAS" or word == "SAMX":
                count += 1

    # Vertical and reversed vertical
    for r in range(rows - 3):
        for c in range(cols):
            word = "".join(grid[r : r + 4, c])
            if word == "XMAS" or word == "SAMX":
                count += 1

    # Diagonals (NW-SE and NE-SW)
    for r in range(rows - 3):
        for c in range(cols - 3):
            # NW-SE diagonal
            word = "".join(grid[r + i, c + i] for i in range(4))
            if word == "XMAS" or word == "SAMX":
                count += 1

            # NE-SW diagonal
            word = "".join(grid[r + i, c + 3 - i] for i in range(4))
            if word == "XMAS" or word == "SAMX":
                count += 1

    return count


def preprocess_input(input_text: str):
    grid = create_numpy_grid(input_text)
    return grid


def first(wordsearch: np.ndarray) -> int:
    return count_xmas(wordsearch)


def second(wordsearch: np.ndarray) -> int:
    # 5568 too high
    return count_x_mas(wordsearch)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=4, year=2024)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
