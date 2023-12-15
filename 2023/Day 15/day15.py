from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

def HASH(chars: str) -> int:
    current_value = 0
    for char in chars:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value
    

def preprocess_input(input_text: str):
    input_text = input_text.replace('\n', '')
    sequences = input_text.split(',')
    return sequences


def first(sequences) -> int:
    return sum(HASH(seq) for seq in sequences)


def second(sequences) -> int:
    boxes = [[] for _ in range(256)]

    for seq in sequences:
        if '-' in seq:
            label = seq[:-1]
            box_number = HASH(label)
            boxes[box_number] = [lens for lens in boxes[box_number] if lens[0] != label]

        else:
            label = seq[:-2]
            focal_length = seq[-1]
            box_number = HASH(label)
            for i, lens in enumerate(boxes[box_number]):
                if lens[0] == label:
                    boxes[box_number][i][1] = focal_length
                    break
            else:
                boxes[box_number].append([label, focal_length])

    total = 0
    for i, box in enumerate(boxes, 1):
        for j, (label, focal_length) in enumerate(box, 1):
            focusing_power = i * j * int(focal_length)
            total += focusing_power
    return total



if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=15, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
