from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
from scipy import signal

KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def get_removable_stacks(paper_grid: np.ndarray) -> np.ndarray:
    adjacent_stacks = signal.convolve2d(paper_grid, KERNEL, mode="same")
    return np.logical_and(adjacent_stacks < 4, paper_grid)


def remove_stacks(paper_grid: np.ndarray, to_be_removed: np.ndarray) -> np.ndarray:
    return np.logical_and(paper_grid, ~to_be_removed)


def count_removed_stacks(paper_grid: np.ndarray) -> int:
    original_count = np.sum(paper_grid)
    while True:
        removable_stacks = get_removable_stacks(paper_grid)
        if np.sum(removable_stacks) == 0:
            break
        paper_grid = remove_stacks(paper_grid, removable_stacks)
    remaining_count = np.sum(paper_grid)
    return original_count - remaining_count


def preprocess_input(input_text: str) -> np.ndarray:
    grid = create_numpy_grid(input_text)
    return grid == "@"


def first(paper_grid: np.ndarray) -> int:
    return np.sum(get_removable_stacks(paper_grid))


def second(paper_grid: np.ndarray) -> int:
    return count_removed_stacks(paper_grid)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=4, year=2025)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
