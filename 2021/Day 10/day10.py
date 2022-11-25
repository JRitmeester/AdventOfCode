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

from aoc_util.helpers import load_input_data


def remove_kernels(line):
    matching_brackets = r"\{\}|\(\)|\[\]|\<\>"
    # Keep searching for kernels if they're there.
    while np.array((re.findall(matching_brackets, line))).size != 0:
        # Remove any found kernels.
        line = re.sub(matching_brackets, "", line)

    return line


def preprocess_input(input_text: str):
    return np.array(input_text.split("\n"))


def first(input) -> int:
    total = 0
    incomplete = []
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}

    for line in input:
        copy = line
        copy = remove_kernels(copy)
        illegal_chars = re.findall("\]|\)|>|}", copy)
        if len(illegal_chars) > 0:
            total += scores[illegal_chars[0]]
        else:
            incomplete.append(copy)
    return total, incomplete


def second(incomplete_lines: list[str]) -> int:
    totals = []
    scores = {")": 1, "]": 2, "}": 3, ">": 4}
    opposites = {"[": "]", "<": ">", "(": ")", "{": "}"}

    for line in incomplete_lines:
        total = 0
        mirrored = "".join([opposites[char] for char in reversed(line)])
        for char in mirrored:
            total = total * 5 + scores[char]
        totals.append(total)

    return int(np.median(totals))


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=10, year=2021)
    preprocessed_input = preprocess_input(original_input)
    answer_first, incomplete = first(preprocessed_input)
    print("The answer to part 1 is:", answer_first)
    print("The answer to part 2 is:", second(incomplete))
