from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import (
    load_input_data,
    create_numpy_grid,
    get_2d_index,
    print_timing,
)
import numpy as np
import re
from pprint import pprint
import matplotlib.pyplot as plt

np.random.seed(42)


def render_map(map: np.ndarray):
    """Render the map with a unique colour for each frequency. Not very useful, but fun to look at.

    Args:
        grid (np.ndarray): _description_
    """
    # Create an array to store the RGB values for the image
    render = np.zeros((*map.shape, 3), dtype=float)

    # Extract unique characters from the grid
    unique_characters = np.unique(map)

    # Assign a unique random color to each character
    color_map = {
        char: np.random.rand(3)  # Generate RGB values in the range [0, 1]
        for char in unique_characters
    }

    # Assign a specific color for empty or background characters (e.g., ".")
    color_map["."] = np.array([0, 0, 0])  # Black for background

    # Map characters to colors
    for row_idx in range(map.shape[0]):
        for col_idx in range(map.shape[1]):
            render[row_idx, col_idx] = color_map[map[row_idx, col_idx]]

    # Display the rendered grid
    plt.imshow(render)
    plt.axis("off")
    plt.show()


def generate_antinode_map(
    frequency: str, map: np.ndarray, use_harmonics: bool
) -> np.ndarray:
    # Find the 2D location of each antenna
    antennas = get_2d_index(map, frequency)

    # Keep track if there is an antinode. It doesn't matter of which frequency.
    antinode_map = np.zeros_like(map, dtype=bool)
    rows, cols = map.shape

    for antenna_A in antennas:
        for antenna_B in antennas:
            if antenna_A == antenna_B:
                continue
            A = np.asarray(antenna_A)
            B = np.asarray(antenna_B)

            # Calculate the relative position, and subtract it i times from antenna A's position.
            # If using harmonics, include also the antenna's position itself
            ith_harmonic = 0 if use_harmonics else 1
            while True:

                # Calculate the ith antinode's position.
                antinode_position = A - (ith_harmonic * (B - A))

                # Discard the antinode if it is out of bounds.
                if (
                    antinode_position[0] < 0
                    or antinode_position[0] >= rows
                    or antinode_position[1] < 0
                    or antinode_position[1] >= cols
                ):
                    break

                # Mark the position of the antinode.
                antinode_map[tuple(antinode_position)] = True

                # If not using harmonics, you're done after 1 iteration where i=1.
                if not use_harmonics:
                    break

                ith_harmonic += 1

    return antinode_map


def preprocess_input(input_text: str):
    map = create_numpy_grid(input_text)
    return map


@print_timing  # 0.00298325 seconds
def first(map: np.ndarray) -> int:
    all_antinodes = np.zeros_like(map, dtype=bool)
    frequencies = np.unique(map)
    for frequency in frequencies:
        if frequency == ".":
            continue
        antinode_map = generate_antinode_map(frequency, map, use_harmonics=False)
        all_antinodes = all_antinodes | antinode_map  # Overlap each map
    return np.sum(all_antinodes)


@print_timing  # 0.00619133 seconds
def second(map: np.ndarray) -> int:
    all_antinodes = np.zeros_like(map, dtype=bool)
    # antinode_maps = {freq: np.zeros_like(map) for freq in np.unique(map)}
    frequencies = np.unique(map)
    for frequency in frequencies:
        if frequency == ".":
            continue
        antinode_map = generate_antinode_map(frequency, map, use_harmonics=True)
        all_antinodes = all_antinodes | antinode_map  # Overlap each map

    render_map(map)
    return np.sum(all_antinodes)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=8, year=2024)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
