from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from pprint import pprint

def preprocess_input(input_text: str):
    lines = input_text.split('\n')
    
    return lines


def first(lines) -> int:

    grid = np.array([list(x) for x in lines])

    non_symbols = ['1','2','3','4','5','6','7','8','9','0','.']
    symbol_mask = np.ones_like(grid).astype(bool)
    
    for ns in non_symbols:
        symbol_mask = np.logical_and(symbol_mask, grid != ns)

    symbol_coords = np.where(symbol_mask)
    symbol_coords = list(zip(*symbol_coords))

    ###

    all_nums = []
    for y, line in enumerate(lines):
        num = []
        coords = []
        last_char_numeric = False

        for x, char in enumerate(line):
            if char.isnumeric():
                num.append(char)
                last_char_numeric = True
                coords.append((y,x))
            else:
                if last_char_numeric:
                    # Number has ended
                    all_nums.append((int(''.join(num)), coords))
                    num = []
                    coords = []
                last_char_numeric = False

        # Edge case for numbers at the end of the line
        if last_char_numeric:
            all_nums.append((int(''.join(num)), coords))


    NEIGHBOURS = [(-1, -1), (-1, -0), (-1, 1), 
                  (0, -1), (0, 1), 
                  (1, -1), (1, 0), (1, 1)]
    
    valid_nums = []
    for (sy, sx) in symbol_coords:
        for (ny, nx) in NEIGHBOURS:
            y = sy + ny
            x = sx + nx
            for num_coords in all_nums:
                num, coords = num_coords
                try:
                    coords_idx = coords.index((y,x))
                    valid_nums.append(num)
                    all_nums.remove(num_coords)
                    break
                except ValueError:
                    pass

    return np.sum(valid_nums)

def second(lines) -> int:
    grid = np.array([list(x) for x in lines])

    gear_mask = np.where(grid == '*')
    gear_coords = list(zip(*gear_mask))

    ###

    all_nums = []
    for y, line in enumerate(lines):
        num = []
        coords = []
        last_char_numeric = False

        for x, char in enumerate(line):
            if char.isnumeric():
                num.append(char)
                last_char_numeric = True
                coords.append((y,x))
            else:
                if last_char_numeric:
                    # Number has ended
                    all_nums.append((int(''.join(num)), coords))
                    num = []
                    coords = []
                last_char_numeric = False

        # Edge case for numbers at the end of the line
        if last_char_numeric:
            all_nums.append((int(''.join(num)), coords))


    NEIGHBOURS = [(-1, -1), (-1, -0), (-1, 1), 
                  (0, -1), (0, 1), 
                  (1, -1), (1, 0), (1, 1)]
    
    gear_data = []
    for (sy, sx) in gear_coords:
        gear_numbers = []
        for (ny, nx) in NEIGHBOURS:
            y = sy + ny
            x = sx + nx
            for num_coords in all_nums:
                num, coords = num_coords
                try:
                    coords_idx = coords.index((y,x))
                    gear_numbers.append(num)
                    all_nums.remove(num_coords)
                    break
                except ValueError:
                    pass
        if len(gear_numbers) > 1:
            gear_data.append(np.prod(gear_numbers))

    return sum(gear_data)

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=3, year=2023)
    preprocessed_input = preprocess_input(original_input)
    # print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
