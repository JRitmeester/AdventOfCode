from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

num_dict = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

def find_calibration_digit(line):
    digits = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)
    digits = [num_dict.get(digit, digit) for digit in digits]
    number = int(digits[0] + digits[-1])
    return number

def preprocess_input(input_text: str):
    lines = input_text.split("\n")
    return lines

def first(lines) -> int:
    return np.sum([find_calibration_digit(line) for line in lines])

def second(lines) -> int:
    return np.sum([find_calibration_digit(line) for line in lines])


if __name__ == "__main__":
    original_input_1 = load_input_data(file.parent / "input.txt", day=1, year=2023)
    original_input_2 = load_input_data(file.parent / "input.txt", day=1, year=2023)

    preprocessed_input_1 = preprocess_input(original_input_1)
    preprocessed_input_2 = preprocess_input(original_input_2)

    print("The answer to part 1 is:", first(preprocessed_input_1))
    print("The answer to part 2 is:", second(preprocessed_input_2))
