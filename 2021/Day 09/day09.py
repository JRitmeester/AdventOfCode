import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve2d

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import input_to_np_arr, load_input_data

UP = np.array([[0, 1, 0], [0, -1, 0], [0, 0, 0]])
DOWN = np.flipud(UP)
LEFT = np.array([[0, 0, 0], [1, -1, 0], [0, 0, 0]])
RIGHT = np.fliplr(LEFT)


def preprocess_input(input_text: str, size=(100, 100)):
    return np.array([int(n) for row in input_text.split("\n") for n in row]).reshape(
        size
    )


def get_gradient(input):
    padded_map = np.pad(input, 1, constant_values=10)
    conv_up = convolve2d(padded_map, UP, mode="valid") > 0
    conv_down = convolve2d(padded_map, DOWN, mode="valid") > 0
    conv_left = convolve2d(padded_map, LEFT, mode="valid") > 0
    conv_right = convolve2d(padded_map, RIGHT, mode="valid") > 0
    return conv_up, conv_down, conv_left, conv_right


def find_low_points_coords(input):
    """
    Convolve the padded map with the four structure elements to get a difference map in each direction.
    Then turn these scalar maps into binary maps, and AND them together to find the low points.
    """

    grad_up, grad_down, grad_left, grad_right = get_gradient(input)
    low_points = grad_up & grad_down & grad_left & grad_right
    return np.nonzero(low_points > 0)


def first(input) -> int:
    low_point_values = input[find_low_points_coords(input)]
    risk_sum = sum(low_point_values) + len(low_point_values)
    return risk_sum


def second(input) -> int:
    # Pathfinding = skip
    pass


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=9, year=2021)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
