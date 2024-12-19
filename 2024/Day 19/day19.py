from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint
from tqdm import tqdm


def count_patterns(goal_pattern: str, towels: tuple[str], memo={}):
    """Count the number of ways to form the goal pattern using the towels.

    Args:
        goal_pattern (str): The pattern to form.
        towels (tuple[str]): The towels available.
        memo (dict, optional): The memoization dictionary. Defaults to {}.

    Returns:
        int: The number of ways to form the goal pattern.
    """
    if goal_pattern == "":
        return 1
    if goal_pattern in memo:
        return memo[goal_pattern]

    total = 0
    for towel in towels:
        if goal_pattern.startswith(towel):
            remaining = goal_pattern[len(towel) :]
            total += count_patterns(remaining, towels, memo)

    memo[goal_pattern] = total
    return total


def preprocess_input(input_text: str):
    towels, patterns = input_text.split("\n\n")
    towels = towels.split(", ")
    patterns = patterns.split("\n")
    towels = tuple(sorted(towels, key=len, reverse=True))
    return towels, patterns


def first(towels: tuple[str], patterns: list[str]) -> int:
    total = 0
    for pattern in tqdm(patterns):
        total += count_patterns(pattern, towels) > 0
    return total


def second(towels: list[str], patterns: list[str]) -> int:
    total = 0
    for pattern in tqdm(patterns):
        total += count_patterns(pattern, towels)
    return total


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=19, year=2024)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(*preprocessed_input))
    print("The answer to part 2 is:", second(*preprocessed_input))
