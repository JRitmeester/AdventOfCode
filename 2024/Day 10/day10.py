from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import create_numpy_grid, load_input_data, print_timing, DIRS
import numpy as np
import re
from pprint import pprint

import numpy as np


def follow_path(x, y, previous, trail_ends, map):
    rows, cols = map.shape

    def get(x, y):
        if 0 <= x < cols and 0 <= y < rows:
            return map[y][x]
        return None

    current = get(x, y)
    if current is None or current - previous != 1:
        return
    if current == 9:
        trail_ends.append((x, y))
        return
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        follow_path(x + dx, y + dy, current, trail_ends, map)


def preprocess_input(input_text: str):
    return create_numpy_grid(input_text).astype(int)


def first_and_second(map: np.ndarray) -> int:
    starting_points = np.argwhere(map == 0)
    score_unique = []
    score_rating = []
    for p in starting_points:
        trail_ends = []
        follow_path(p[1], p[0], -1, trail_ends, map)
        score_unique.append(len(set(trail_ends)))
        score_rating.append(len(trail_ends))
    return sum(score_unique), sum(score_rating)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=10, year=2024)
    preprocessed_input = preprocess_input(original_input)
    first_, second_ = first_and_second(preprocessed_input)
    print("The answer to part 1 is:", first_)
    print("The answer to part 2 is:", second_)
