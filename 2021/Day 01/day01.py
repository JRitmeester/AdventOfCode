import sys
from pathlib import Path
import numpy as np

sys.path.append(str(Path.cwd()))
from aoc_util.helpers import load_input_data, input_to_np_arr


def preprocess_input(input_text: str):
    return input_to_np_arr(input_text.split("\n"), dtype=int)


def first(input):
    n_increasing = np.count_nonzero(np.convolve(input, [1, -1], mode="valid") > 0)
    return n_increasing


def second(input):
    sliding_signal = np.convolve(input, [1, 1, 1], mode="valid")
    n_increasing = np.count_nonzero(
        np.convolve(sliding_signal, [1, -1], mode="valid") > 0
    )
    return n_increasing


if __name__ == "__main__":
    original_input = load_input_data(
        Path(__file__).parent / "input.txt", day=1, year=2021
    )
    print("The answer to part 1 is:", first())
    print("The answer to part 2 is:", second())
