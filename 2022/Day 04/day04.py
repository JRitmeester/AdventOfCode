import re
import sys
from pathlib import Path

import numpy as np

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data, print_timing

AND = np.logical_and
XOR = np.logical_xor


@print_timing
def preprocess_input(input_text: str) -> list[tuple[np.ndarray, np.ndarray]]:
    pairs = []
    lines = input_text.split("\n")
    for line in lines:
        # Create binary masks for which sectors each elf has assigned: 6-8 = [0, 0, 0, 0, 0, 0, 1, 1, 1]
        start_1, end_1, start_2, end_2 = [int(n) for n in re.findall("[0-9]+", line)]
        elf1 = np.zeros(100)
        elf1[start_1 : end_1 + 1] = 1
        elf2 = np.zeros(100)
        elf2[start_2 : end_2 + 1] = 1
        pairs.append((elf1, elf2))

    return pairs


def bitwise_contains(a: np.ndarray, b: np.ndarray) -> bool:
    # Using bitwise operators, find if the smaller range fits inside the larger range, using an AND gate
    # e.g. 00011000 AND 01111110 = 00011000
    # Then check if the result is equal to the smaller mask using an XOR gate.
    # e.g. 00011000 XOR 00011000 = 00000000 -> not any (00000000) = True = equal
    #  but 00011000 XOR 11000000 = 11011000 -> not any (11011000) = False = not equal
    # Formula becomes not any((A AND B) XOR A)
    return not any(XOR(AND(a, b), a))


def bitwise_overlap(a: np.ndarray, b: np.ndarray) -> bool:
    return any(AND(a, b))


@print_timing
def first(pairs) -> int:
    total = sum(
        bitwise_contains(elf1, elf2) or bitwise_contains(elf2, elf1)
        for elf1, elf2 in pairs
    )
    return total


@print_timing
def second(pairs) -> int:
    total = sum(bitwise_overlap(elf1, elf2) for elf1, elf2 in pairs)
    return total


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=4, year=2022)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
