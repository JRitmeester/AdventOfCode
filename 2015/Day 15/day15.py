from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

def preprocess_input(input_text: str):
    ingredients = input_text.splitlines()
    values = [list(map(int, re.findall('-?\d+', ing))) for ing in ingredients]
    return np.array(values)


def calculate_max_score(values, calorie_constraint=None):
    """
    Calculate the maximum score given the ingredient values and an optional calorie constraint.
    """
    max_score = 0
    for i in range(101):
        for j in range(101 - i):
            for k in range(101 - i - j):
                l = 100 - i - j - k
                mixture = np.array([i, j, k, l])
                product_properties = np.dot(mixture, values)
                if calorie_constraint is not None and product_properties[-1] != calorie_constraint:
                    continue
                score = np.prod(np.maximum(product_properties[:-1], 0))
                max_score = max(score, max_score)
    return max_score

def first(input_data) -> int:
    return calculate_max_score(input_data)


def second(input_data) -> int:
    return calculate_max_score(input_data, calorie_constraint=500)

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=15, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
