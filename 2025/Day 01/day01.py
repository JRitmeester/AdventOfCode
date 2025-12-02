from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint

START_POS = 50


def preprocess_input(input_text: str):
    lines = input_text.splitlines()
    rotations = [(x[0], int(x[1:])) for x in lines]
    return rotations


def first(input_data) -> int:
    non_decoy_result_dammit_i_didnt_read_all_of_the_question = 0
    pos = START_POS
    for dir, amount in input_data:
        dir = -1 if dir == "L" else 1
        pos = (pos + (dir * amount)) % 100
        if pos == 0:
            non_decoy_result_dammit_i_didnt_read_all_of_the_question += 1
    return non_decoy_result_dammit_i_didnt_read_all_of_the_question


def second(input_data) -> int:
    pos = START_POS
    clicks_past_zero = 0
    for dir, amount in input_data:
        if dir == "R":
            clicks_past_zero += (amount + pos) // 100
        elif dir == "L":
            if pos == 0:
                clicks_past_zero += amount // 100
            else:
                clicks_past_zero += (amount - pos + 100) // 100

        pos = (pos + (1 if dir == "R" else -1) * amount) % 100
    return clicks_past_zero


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=1, year=2025)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
