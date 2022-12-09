import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data, print_timing

UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"


@print_timing
def preprocess_input(input_text: str):
    return input_text


class DeliveryGuy:
    def __init__(self):
        self.position = np.array([0, 0])

    def move(self, dir: np.ndarray) -> None:
        if dir == UP:
            self.position += [0, -1]
        elif dir == DOWN:
            self.position += [0, 1]
        elif dir == LEFT:
            self.position += [-1, 0]
        elif dir == RIGHT:
            self.position += [1, 0]

    def deliver(self, grid: np.ndarray, xoffset: int, yoffset: int) -> np.ndarray:
        grid[self.position[0] + xoffset, self.position[1] + yoffset] += 1
        return grid


@print_timing
def first(input_data) -> int:
    up_count, down_count, right_count, left_count = (
        input_data.count(UP),
        input_data.count(DOWN),
        input_data.count(LEFT),
        input_data.count(RIGHT),
    )

    grid = np.zeros((left_count + right_count, up_count + down_count))
    grid[right_count, down_count] = 1

    santa = DeliveryGuy()

    for step in input_data:
        santa.move(step)
        santa.deliver(grid, right_count, down_count)

    plt.imshow(grid)
    plt.show()
    return np.count_nonzero(grid)


@print_timing
def second(input_data) -> int:
    print(input_data)
    up_count, down_count, right_count, left_count = (
        input_data.count(UP),
        input_data.count(DOWN),
        input_data.count(LEFT),
        input_data.count(RIGHT),
    )

    grid = np.zeros((left_count + right_count, up_count + down_count))
    santa = DeliveryGuy()
    robot = DeliveryGuy()
    grid[right_count, down_count] = 1

    santas_turn = True
    for step in input_data:
        deliverer = santa if santas_turn else robot
        deliverer.move(step)
        deliverer.deliver(grid, right_count, down_count)
        santas_turn = not santas_turn

    plt.imshow(grid)
    plt.show()
    return np.count_nonzero(grid)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=3, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
