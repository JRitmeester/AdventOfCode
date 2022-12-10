import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data, print_timing


def get_register_values_at_cycle(instructions: list[str]) -> list[int]:
    register_values = [1]  # Start off with the value of 1.
    for instruction in instructions:
        if "addx" in instruction:
            value = int(instruction.split(" ")[1])
            register_values.extend([register_values[-1], register_values[-1] + value])
        else:
            register_values.append(register_values[-1])
    return register_values


@print_timing
def preprocess_input(input_text: str):
    return get_register_values_at_cycle(input_text.split("\n"))


@print_timing
def first(register_values) -> int:
    # Subtract one to compensate for the initial value, and one for the fact that the number is updated at the END
    # of the cycle.
    total_signal_strength = sum(
        [cycle * register_values[cycle - 2] for cycle in range(20, 260, 40)]
    )
    return total_signal_strength


@print_timing
def second(register_values) -> int:
    crt = np.zeros((6, 40))
    for crt_y in range(6):
        for crt_x in range(40):
            sprite_x = register_values[
                crt_x + crt_y * 40
            ]  # Calculate the center of the three pixel wide sprite.
            if sprite_x - 1 <= crt_x <= sprite_x + 1:
                crt[crt_y][crt_x] = 1

    # Use official AoC background blue and highlight green for the display
    cmap = colors.ListedColormap(["#0E0E23", "#01CC01"])
    plt.imshow(crt, cmap=cmap, norm=colors.BoundaryNorm([0, 0.5, 1], cmap.N))
    plt.show()


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=10, year=2022)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
