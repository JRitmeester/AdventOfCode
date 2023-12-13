from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

def preprocess_input(input_text: str):
    drawings = input_text.split('\n\n')
    new_drawings = []
    for drawing in drawings:
        drawing = np.array([list(line) for line in drawing.split('\n')])
        new_drawings.append(drawing)

    return new_drawings

def find_identical_lines(drawing: np.ndarray, allow_one_difference: bool):
    """Find two rows in the drawing that are identical."""
    row_indices = []
    for y in range(drawing.shape[0]-1):
        row_a = drawing[y]
        row_b = drawing[y+1]
        n_differences = np.sum(row_a != row_b)
        if n_differences == 0 or (n_differences == 1 and allow_one_difference):
            row_indices.append(y)
    return row_indices


def get_mirror_index_simple(drawing):
    indices = find_identical_lines(drawing, allow_one_difference=False)
    for index in indices:
        offset = 0
        while True:
            index_a = index - offset
            index_b = index + 1 + offset
            
            if index_a < 0 or index_b > drawing.shape[0]-1:  # Out of bounds, done checking
                return index
            
            row_a = drawing[index_a]
            row_b = drawing[index_b]
            n_differences = np.sum(row_a != row_b)  # Element-wise checking if all symbols are the same.

            if n_differences != 0:  # Found a difference, should stop checking and move on to the next possible index.
                break

            offset += 1
    else:
        return None

def get_mirror_index_complex(drawing):
    indices = find_identical_lines(drawing, allow_one_difference=True)
    for index in indices:
        offset = 0
        smudge_is_fixed = False

        while True:
            index_a = index - offset
            index_b = index + 1 + offset
            
            if index_a < 0 or index_b > drawing.shape[0]-1:  # Out of bounds, done checking
                if smudge_is_fixed:
                    return index
                else:
                    break
            
            row_a = drawing[index_a]
            row_b = drawing[index_b]
            n_differences = np.sum(row_a != row_b)  # Element-wise checking if all symbols are the same.

            if n_differences == 1 and not smudge_is_fixed:
                smudge_is_fixed = True

            if n_differences > 1:
                break

            offset += 1

    else:
        return None

def get_mirror_score(drawing, must_fix_smudge: bool):
    if must_fix_smudge:
        f = get_mirror_index_complex
    else:
        f = get_mirror_index_simple

    is_horizontal = True
    index = f(drawing)
    if index is None:
        index = f(np.rot90(drawing, k=3))
        is_horizontal = False
    
    if is_horizontal:
        return 100*(index+1)
    else:
        return (index+1)
    

def first(drawings) -> int:
    total = 0
    for drawing in drawings:
        total += get_mirror_score(drawing, must_fix_smudge=False)

    return total


def second(drawings) -> int:
    total = 0
    for drawing in drawings:
        total += get_mirror_score(drawing, must_fix_smudge=True)

    return total

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=13, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
