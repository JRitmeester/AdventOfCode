from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint
import re


def remove_kernels(line):
    kernels = ["()", "{}", "[]", "<>"]

    # Keep searching for kernels if they're there.
    while np.array((re.findall(r"(\(\))|(\[\])|(<>)|({})", line))).size != 0:
        for kernel in kernels:
            # Remove any found kernels.
            line = re.sub(r"(\(\))|(\[\])|(<>)|({})", "", line)

    return line


def main():
    input_raw = (Path(__file__).parent / "input.txt").read_text()
    lines = np.array(input_raw.split("\n")[:-1])

    incomplete = []  # For part 2

    # Part 1
    total = 0
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}

    for i, line in enumerate(lines):
        copy = line
        copy = remove_kernels(copy)
        illegal_chars = re.findall("\]|\)|>|}", copy)
        if len(illegal_chars) > 0:
            total += scores[illegal_chars[0]]
        else:
            incomplete.append(copy)

    print("Answer part 1:", total)

    # Part 2
    totals = []
    scores = {")": 1, "]": 2, "}": 3, ">": 4}
    opposites = {"[": "]", "<": ">", "(": ")", "{": "}"}

    for line in incomplete:
        # print(line)
        total = 0
        mirrored = "".join([opposites[char] for char in reversed(line)])
        for char in mirrored:
            total = total * 5 + scores[char]
        totals.append(total)

    print("Answer part 2:", int(np.median(totals)))


if __name__ == "__main__":
    main()
