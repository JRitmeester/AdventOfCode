from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from pprint import pprint
import functools
from pprint import pprint

def preprocess_input(input_text: str):
    lines = input_text.splitlines()
    puzzle = []
    for line in lines:
        springs, config = line.split()
        config = tuple(map(int, config.split(',')))
        puzzle.append((springs, config))

    return puzzle

def is_valid(puzzle, config):
    if len(config) == 0 and puzzle.count('#') == 0:
        return True
    
    padded_puzzle = padded_puzzle = f".{puzzle}."

    for ith_digit, digit in enumerate(config):
        location = padded_puzzle.find(f".{digit*'#'}.")
        if location > -1:
            before = puzzle[:location]
            before_config = config[:ith_digit]
            after = puzzle[location + digit:]
            after_config = config[ith_digit+1:]
            return is_valid(before, before_config) and is_valid(after, after_config)
        else:
            return False
        
    return False


def get_variants(puzzle):
    variants = ['']
    for char in puzzle:
        if char != '?':
            variants = [variant+char for variant in variants]
        else:
            variants_a = [variant+'#' for variant in variants]
            variants_b = [variant+'.' for variant in variants]
            variants = variants_a + variants_b

    return variants


def first(puzzles) -> int:
    total = 0
    for puzzle, config in puzzles:
        valid_variants = 0
        for variant in get_variants(puzzle):
            valid_variants += is_valid(variant, config)
        print(puzzle, valid_variants)
        total += valid_variants

    return total
        

def second(puzzle) -> int:
    pass

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=12, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
