from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt


r_cap = 12
g_cap = 13
b_cap = 14

def preprocess_input(input_text: str):
    games = input_text.split('\n')
    return games

def get_r_g_b_from_subset(subset: str) -> tuple[int, int , int]:
    red_count = re.findall('(\d+) red', subset)
    if len(red_count) > 0:
        red_count = int(red_count[0])
    else:
        red_count = 0

    green_count = re.findall('(\d+) green', subset)
    if len(green_count) > 0:
        green_count = int(green_count[0])
    else:
        green_count = 0

    blue_count = re.findall('(\d+) blue', subset)
    if len(blue_count) > 0:
        blue_count = int(blue_count[0])
    else:
        blue_count = 0

    return (red_count, green_count, blue_count)

def first(games) -> int:

    valid_game_ids = []

    for game in games:
        game_id = int(re.findall(r'(\d+): ', game)[0])
        game_config = re.findall(r': (.*)', game)[0]
        subsets = game_config.split('; ')

        for subset in subsets:
            red_count, green_count, blue_count = get_r_g_b_from_subset(subset)            
            if red_count > r_cap or green_count > g_cap or blue_count > b_cap:
                break
        else:
            valid_game_ids.append(game_id)

    return np.sum(valid_game_ids)


def second(games) -> int:

    powers = []

    for game in games:
        game_config = re.findall(r': (.*)', game)[0]
        subsets = game_config.split('; ')

        max_r = 0
        max_g = 0
        max_b = 0

        for subset in subsets:
            red_count, green_count, blue_count = get_r_g_b_from_subset(subset)   
            max_r = max(max_r, red_count)
            max_g = max(max_g, green_count)
            max_b = max(max_b, blue_count)
        
        powers.append(max_r * max_g * max_b)
    return np.sum(powers)

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=2, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
