from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

def preprocess_input(input_text: str):
    time, distance = input_text.splitlines()
    return (time, distance)

def calculate_ways_to_win(time: int, distance: int) -> int:
    has_won = 0
    for ms in range(time+1):
        speed = ms
        travel_time = time - ms
        traveled_distance = travel_time * speed
        if traveled_distance > distance:
            has_won += 1
    return has_won

def first(input_data) -> int:
    time, distance = input_data
    times = list(map(int, re.findall('\d+', time)))
    distances = list(map(int, re.findall('\d+', distance)))
    ways_to_win = [calculate_ways_to_win(time, distance) for time, distance in list(zip(*[times, distances]))]
    return np.prod(ways_to_win)
            

def second(input_data) -> int:
    time, distance = input_data
    time = int(''.join([x for x in time.split(':')[-1] if x != ' ']))
    distance = int(''.join([x for x in distance.split(':')[-1] if x != ' ']))
    return calculate_ways_to_win(time, distance)
    

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=6, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
