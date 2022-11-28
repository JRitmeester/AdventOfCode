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

from aoc_util.helpers import load_input_data

index_kernel = np.array([2**i for i in range(9)]).reshape((3, 3))


def get_new_pixel_indices(image: np.ndarray):
    pixel_indices = convolve2d(
        image, index_kernel, mode="valid"
    )  # Convolve the kernel to get the decimal number from binary pixels.
    return pixel_indices


def retrieve_pixels(sequence, pixel_indices: np.ndarray) -> np.ndarray:
    new_image = np.vectorize(lambda x: sequence[x])(
        pixel_indices
    )  # Look up the pixel by index from the sequence.
    return new_image


def enhance_image(sequence, image: np.ndarray, n_times: int) -> np.ndarray:
    all_images = [image.copy()]

    for _ in range(n_times):
        pixel_indices = get_new_pixel_indices(image)
        image = retrieve_pixels(sequence, pixel_indices)
        all_images.append(image.copy())

    return image


def preprocess_input(input_text: str, shape: tuple = (100, 100)):
    sequence, image = input_text.split("\n\n")
    sequence = np.array(list(sequence)) == "#"

    image = np.array([px for px in "".join(image.split("\n"))]) == "#"
    image = image.reshape(shape)
    image = np.pad(
        image, 100, mode="constant", constant_values=0
    )  # Add "infinite" padding of zero values.
    return sequence, image


def first(input) -> int:
    sequence, image = input
    image = enhance_image(sequence, image, n_times=2)
    return np.sum(image)


def second(input) -> int:
    sequence, image = input
    image = enhance_image(sequence, image, n_times=50)
    return np.sum(image)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=20, year=2021)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
