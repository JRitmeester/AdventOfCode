import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data


def create_map(lines: list, include_diagonal: bool, size=(2000, 2000)):
    grid = np.zeros(size)

    # max_x = 0
    # max_y = 0

    for line in lines:
        start, end = np.array(line).astype(float)
        delta = end - start
        lengths = np.abs(delta)
        dir = delta / np.max(lengths)

        if not include_diagonal:
            if np.sum(np.abs(dir)) != 1:
                continue

        n_steps = np.abs(np.max(lengths).astype(int))
        for step in range(n_steps + 1):
            current = (start + step * dir).astype(int)
            grid[current[1], current[0]] += 1
            # max_x = max(max_x, current[0])
            # max_y = max(max_y, current[1])

    return grid.astype(int)


def preprocess_input(original_input: str) -> list[tuple[int]]:
    input_split = original_input.split("\n")
    lines = [
        [tuple(int(el) for el in point.split(",")) for point in line.split(" -> ")]
        for line in input_split
    ]
    return lines


def first(lines, do_plot=False):
    grid = create_map(lines, include_diagonal=False)

    if do_plot:
        plt.imshow(grid)
        plt.show()

    return np.count_nonzero(grid > 1)


def second(lines, do_plot=False):
    grid = create_map(lines, include_diagonal=True)

    if do_plot:
        plt.imshow(grid)
        plt.show()

    return np.count_nonzero(grid > 1)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=5, year=2021)
    input_ = preprocess_input(original_input)
    print("The answer to part 1 is:", first(input_))
    print("The answer to part 2 is:", second(input_))
