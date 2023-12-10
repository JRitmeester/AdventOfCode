from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from pprint import pprint

DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Up  # Right  # Down  # Left


def traverse_pipes(grid, start_dir_index: int, start_normal_inward_vector_index: int):
    # J|L
    # -.-
    # 7|F
    position = np.argwhere(grid == "S")[0]  # (y, x)
    position_history = [tuple(position)]
    shape_history = ["S"]

    dir_index = start_dir_index
    dir = DIRS[dir_index]

    empty_tiles = []

    # Construct the position history for the second iteration to check against.
    while True:
        position += dir
        y, x = position
        shape = grid[y, x]

        position_history.append(tuple(position))
        shape_history.append(shape)

        if shape == "S":
            break


        if shape in ["7", "F", "J", "L"]:  # Direction needs to change
            if (
                (dir_index == 0 and shape == "7")
                or (dir_index == 1 and shape == "J")
                or (dir_index == 2 and shape == "L")
                or (dir_index == 3 and shape == "F")
            ):
                dir_index -= 1
            elif (
                (dir_index == 0 and shape == "F")
                or (dir_index == 1 and shape == "7")
                or (dir_index == 2 and shape == "J")
                or (dir_index == 3 and shape == "L")
            ):
                dir_index += 1
            dir_index %= 4
            dir = DIRS[dir_index]

    position = np.argwhere(grid == "S")[0]  # (y, x)
    dir = DIRS[start_dir_index]
    normal_inward_vector_index = start_normal_inward_vector_index
    normal_inward_vector = DIRS[normal_inward_vector_index]

    while True:
        position += dir
        y, x = position
        shape = grid[y, x]

        if shape == "S":
            break

        normals = [normal_inward_vector]

        if shape in ["7", "F", "J", "L"]:  # Direction needs to change
            if (
                (dir_index == 0 and shape == "7")
                or (dir_index == 1 and shape == "J")
                or (dir_index == 2 and shape == "L")
                or (dir_index == 3 and shape == "F")
            ):
                dir_index -= 1
                normal_inward_vector_index -= 1
            elif (
                (dir_index == 0 and shape == "F")
                or (dir_index == 1 and shape == "7")
                or (dir_index == 2 and shape == "J")
                or (dir_index == 3 and shape == "L")
            ):
                dir_index += 1
                normal_inward_vector_index += 1
            dir_index %= 4
            normal_inward_vector_index %= 4
            dir = DIRS[dir_index]
            normal_inward_vector = DIRS[normal_inward_vector_index]
            normals.append(normal_inward_vector)

        for normal in normals:
            ray_start = np.array(position)
            for i in range(1, 141):  # Nasty alternative to a while loop with an index
                ray_position = ray_start + i * np.array(normal)

                ry, rx = ray_position
                if ry < 0 or ry >= grid.shape[0] or rx < 0 or rx >= grid.shape[1]:
                    break
                
                char_at_ray = grid[ry, rx]
                if tuple(ray_position) not in position_history:
                    if tuple(ray_position) not in empty_tiles:
                        empty_tiles.append(tuple(ray_position))
                else:
                    break
    pprint(empty_tiles)
    return (len(position_history)) // 2, len((empty_tiles))


def preprocess_input(input_text: str):
    size = len(input_text.splitlines())
    chars = [char for char in input_text if char != "\n"]
    grid = np.array(chars).reshape((size, size))
    return grid


if __name__ == "__main__":
    # input_file = "example_input.txt"
    # input_file = "example_input_2.txt"
    # input_file = "example_input_3.txt"
    # input_file = "example_input_4.txt"
    input_file = "input.txt"
    # input_file = "ellis.txt"

    original_input = load_input_data(file.parent / input_file, day=10, year=2023)
    grid = preprocess_input(original_input)

    if input_file == "example_input.txt":
        dir_index = 1
        normal_dir_index = 2
    elif input_file == "example_input_2.txt":
        dir_index = 1
        normal_dir_index = 2
    elif input_file == "example_input_3.txt":
        dir_index = 1
        normal_dir_index = 0
    elif input_file == "example_input_4.txt":
        dir_index = 2
        normal_dir_index = 3
    elif input_file == "input.txt":
        dir_index = 3
        normal_dir_index = 2
    elif input_file == "ellis.txt":
        dir_index = 0
        normal_dir_index = 3

    answers = traverse_pipes(grid, dir_index, normal_dir_index)
    print("The answer to part 1 is:", answers[0])
    print("The answer to part 2 is:", answers[1])
