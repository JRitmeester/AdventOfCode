import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


def main():
    input_raw = (Path(__file__).parent / "input.txt").read_text()
    numbers = np.array(input_raw.split("\n")[:-1]).astype(np.int)

    num_increasing = np.count_nonzero(np.convolve(numbers, [1, -1], mode="valid") > 0)
    print("Answer part 1:", num_increasing)

    sliding_signal = np.convolve(numbers, [1, 1, 1], mode="valid")
    num_increasing = np.count_nonzero(
        np.convolve(sliding_signal, [1, -1], mode="valid") > 0
    )
    print("Answer part 2:", num_increasing)


if __name__ == "__main__":
    main()
