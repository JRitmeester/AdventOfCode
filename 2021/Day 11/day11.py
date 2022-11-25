import sys
from pathlib import Path
from pprint import pprint

import imageio.v2 as imageio
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

# Is it octopi, octopuses or something else? In this house, it is octos.
# There is a GIF export in here, but I'm not entirely sure the result is correct.
# The answers are correct, though.


def create_gif(image_folder: Path, name: str):
    images = [imageio.imread(file) for file in image_folder.glob("*.png")]
    imageio.mimsave(image_folder / name, images)


def save_image(image_arr, folder, name):
    plt.imshow(image_arr)
    plt.savefig(folder / name)
    plt.close()


def step(octos):
    # Add a charge to all octos.
    octos += 1

    # Keep track of octos that have already flashed.
    has_flashed = np.zeros_like(octos, dtype=bool)

    # Find the positions of octos with a charge above 9.
    charged_octos = list(zip(*np.nonzero(octos > 9)))

    flashes = 0

    while True:
        for y, x in charged_octos:
            if not has_flashed[y, x]:
                # Add a charge to the 3x3 neighbourhood.
                octos[max(y - 1, 0) : y + 2, max(x - 1, 0) : x + 2] += 1
                has_flashed[y, x] = True
                flashes += 1

        # Check for octos that are now charged.
        charged_octos = list(zip(*np.nonzero(np.multiply(octos, ~has_flashed) > 9)))

        # If no charged octos are found, quit.
        if len(charged_octos) == 0:
            break

    # Set the discharged octos to 0.
    octos = np.multiply(octos, ~has_flashed)
    return octos, flashes


def preprocess_input(input_text: str):
    return np.array(
        [[int(energy) for energy in line] for line in input_text.split("\n")]
    )


def first(input, make_gif: bool = False) -> int:
    make_gif = False

    folder = Path(__file__).parent / "images_part_1"
    if make_gif:
        folder.mkdir(exist_ok=True)
        save_image(octos, folder, "0.png")

    # Start simulating the flashes for 100 steps.
    octos = input
    total = 0
    for i in range(100):
        octos, flashes = step(octos)
        if make_gif:
            save_image(octos, folder, f"{i+1}.png")
        total += flashes

    if make_gif:
        create_gif(folder, "part1.gif")

    return total


def second(input, make_gif: bool = False) -> int:
    octos = input

    make_gif = True
    folder = Path(__file__).parent / "images_part_2"
    if make_gif:
        folder.mkdir(exist_ok=True)
        save_image(octos, folder, "0.png")

    steps = 0
    while True:
        steps += 1
        octos, _ = step(octos)

        if make_gif:
            save_image(octos, folder, f"{steps}.png")

        if np.sum(octos) == 0:
            break

    create_gif(folder, "part2.gif")
    # Test ran fine with returned value, but puzzle need another +1.
    return steps


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=11, year=2021)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input, make_gif=False))
    print("The answer to part 2 is:", second(preprocessed_input, make_gif=False))
