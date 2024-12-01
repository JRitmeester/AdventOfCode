from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
from collections import Counter
from aoc_util.helpers import print_timing


def preprocess_input(input_text: str):
    numbers = [int(x) for x in input_text.split()]
    left_list = []
    right_list = []

    put_in_left = True
    for n in numbers:
        if put_in_left:
            left_list.append(n)
        else:
            right_list.append(n)
        put_in_left = not put_in_left

    return left_list, right_list


@print_timing
def first(input_data: list[list[int]]) -> int:
    left_list, right_list = input_data[0], input_data[1]

    # Sort the lists, take the absolute difference piece-wise, and sum the results.
    total = np.sum(np.abs(np.sort(left_list) - np.sort(right_list)))

    # Equivalent to:
    # total = 0
    # for l, r in zip(left_list, right_list):
    #     diff = abs(l - r)
    #     total += diff

    return total


@print_timing
def second(input_data) -> int:
    left_list, right_list = input_data[0], input_data[1]
    counts = Counter(right_list)
    similarity_score = sum([l * counts[l] for l in left_list])
    return similarity_score


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=1, year=2024)

    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
