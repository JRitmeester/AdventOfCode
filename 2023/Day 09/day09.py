from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

def preprocess_input(input_text: str):
    lines = input_text.splitlines()
    histories = [list(map(int, line.split())) for line in lines]
    return histories

def get_derivatives(history: list[int]):
    derivative = history
    derivatives = [history]  # Keep track of all consecutive derivatives
    while True:
        derivative = np.diff(derivative)  # Calculate the next order derivative
        derivatives.append(derivative)
        if np.all((derivative) == 0):
            break
    return derivatives
    
def first(histories) -> int:
    # Placeholder value at the end of each sequence is the placeholder
    # value of the last sequence + the last existing value in the current sequence

    # Intentional annoying oneliner because I can...
    return sum([sum(d[-1] for history in histories for d in reversed(get_derivatives(history)))])



def second(histories) -> int:
    new_values = []
    for history in histories:

        # Placeholder value at the start of each sequence is the first digit of the current
        # sequence - the placeholder digit of the previous sequence.
        new_value = 0  
        for d in reversed(get_derivatives(history)):
            new_value = d[0] - new_value

        new_values.append(new_value)
        
    return sum(new_values)

# ChatGPT generated oneliner version, just for fun.
# def second(histories) -> int:
#     return sum([(lambda nv: [nv := d[0] - nv for d in reversed(get_derivatives(history))][-1])(0) for history in histories])


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=9, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
