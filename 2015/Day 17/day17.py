from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint


def preprocess_input(input_text: str):
    return [int(line) for line in input_text.splitlines()]


def count_combinations(containers, target, index=0, current_sum=0, current_count=0):
    # Base case: if we've exactly hit the target, count this as a valid combination
    if current_sum == target:
        return [
            (current_count, 1)
        ]  # return the number of containers used and one valid combination
    # If we've exceeded the target or reached the end of the list, stop
    if current_sum > target or index == len(containers):
        return []

    # Recursive case:
    # 1. Include the current container
    include = count_combinations(
        containers,
        target,
        index + 1,
        current_sum + containers[index],
        current_count + 1,
    )
    # 2. Exclude the current container
    exclude = count_combinations(
        containers, target, index + 1, current_sum, current_count
    )

    # Return the result from both include and exclude cases
    return include + exclude


def first(containers: list[int], target: int) -> int:
    valid_combinations = count_combinations(containers, target)
    total_combinations = sum(count for _, count in valid_combinations)
    return total_combinations


def second(containers: list[int], target: int) -> int:
    valid_combinations = count_combinations(containers, target)

    # Find the minimum number of containers used in any valid combination
    min_containers = min(count for count, _ in valid_combinations)

    # Count how many combinations use the minimum number of containers
    ways_with_min_containers = sum(
        combination_count
        for count, combination_count in valid_combinations
        if count == min_containers
    )

    return ways_with_min_containers


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=17, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input, 150))
    print("The answer to part 2 is:", second(preprocessed_input, 150))
