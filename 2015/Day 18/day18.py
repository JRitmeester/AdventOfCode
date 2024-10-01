from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint
from scipy import signal

def preprocess_input(input_text: str, size=6):
    return (np.array([char for line in input_text.split('\n') for char in line]).reshape((size,size)) == '#').astype(int)

def evolve(lightboard: np.array) -> np.array:
    kernel = np.array([[1,1,1],[1,0,1],[1,1,1]])
    n_neighbours_on = signal.convolve2d(lightboard, kernel, mode='same', fillvalue=0)
    two_on = n_neighbours_on == 2
    three_on = n_neighbours_on == 3
    lightboard = (lightboard & (two_on | three_on)) | (~lightboard & three_on)
    return lightboard


def first(lightboard, steps=4) -> int:
    for i in range(steps):
        lightboard = evolve(lightboard)
    
    return np.sum(lightboard)

def second(lightboard, steps=5) -> int:
    for i in range(steps):
        lightboard[0, 0] = 1
        lightboard[0, -1] = 1
        lightboard[-1, 0] = 1
        lightboard[-1, -1] = 1
        lightboard = evolve(lightboard)
    lightboard[0, 0] = 1
    lightboard[0, -1] = 1
    lightboard[-1, 0] = 1
    lightboard[-1, -1] = 1
    return np.sum(lightboard)

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=18, year=2015)
    preprocessed_input = preprocess_input(original_input, size=100)
    print("The answer to part 1 is:", first(preprocessed_input, steps=100))
    print("The answer to part 2 is:", second(preprocessed_input, steps=100))
