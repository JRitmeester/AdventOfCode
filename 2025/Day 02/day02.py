from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint


def find_repeating_patterns(i: int, at_least_twice: bool) -> int:
    # ^([1-9][0-9]*)\1$ finds any repeating pattern of digits, of which the repeated part does not start
    # with a 0. The addition of the "+" for part to finds patterns that repeat at least twice.
    if not at_least_twice:
        pattern = r"^([1-9][0-9]*)\1$"
    else:
        pattern = r"^([1-9][0-9]*)\1+$"
    matches = re.match(pattern=pattern, string=str(i))
    if matches:
        return i


def sum_repeating_patterns(ranges: list[tuple[int, int]], at_least_twice: bool):
    repeating_id_sum = 0
    for start, end in ranges:
        for j in range(start, end + 1):
            repeating_id = find_repeating_patterns(j, at_least_twice)
            if repeating_id:
                repeating_id_sum += repeating_id
    return repeating_id_sum


def preprocess_input(input_text: str):
    ranges = []
    for range in input_text.split(","):
        start, end = range.split("-")
        ranges.append((int(start), int(end)))
    return ranges


def first(ranges) -> int:
    return sum_repeating_patterns(ranges, at_least_twice=False)


def second(ranges) -> int:
    return sum_repeating_patterns(ranges, at_least_twice=True)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=2, year=2025)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
