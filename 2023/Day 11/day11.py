from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from pprint import pprint

def preprocess_input(input_text: str):
    size = len(input_text.splitlines())
    chars = [char for char in input_text if char != "\n"]
    grid = np.array(chars).reshape((size, -1))
    return grid


def naive_expand_universe(universe: np.ndarray) -> np.ndarray:
    expanded_universe = universe.copy()
    empty_space = '.' * universe.shape[0]

    for i, row in enumerate(universe):
        if np.all(row == '.'):
            insert_index = (len(expanded_universe) - len(universe)) + i
            expanded_universe = np.insert(expanded_universe, insert_index, empty_space, axis=0)
    
    empty_space = '.' * universe.shape[1]
    for j, col in enumerate(universe.T):
        if np.all(col == '.'):
            insert_index = len(expanded_universe.T) - len(universe.T) + j
            expanded_universe = np.insert(expanded_universe, insert_index, empty_space, axis=1)

    return expanded_universe

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def galaxy_distance(a: tuple[int, int], b: tuple[int, int], rows: list[int], cols: list[int], expansion_size: int):
    ay, ax = a
    by, bx = b
    ay, by = sorted([ay, by])
    ax, bx = sorted([ax, bx])
    
    distance = manhattan_distance(a, b)

    # See what empty space rows exist between the two galaxies
    for row_index in rows:
        if ay < row_index < by:
            distance += expansion_size
    
    # See what empty space columns exist between the two galaxies
    for col_index in cols:
        if ax < col_index < bx:
            distance += expansion_size
    
    return distance

def get_unique_pairs(galaxies: list[tuple]) -> list[tuple[tuple, tuple]]:
    """
    Create unique pairs, upper-triangle only.
    """
    pairs = [(tuple(a), tuple(b)) for i, a in enumerate(galaxies) 
         for j, b in enumerate(galaxies) if i < j]
    return pairs


def first(universe) -> int:
    universe = naive_expand_universe(universe)
    
    # Find the galaxies and their (row, column) coordinates
    galaxies = np.argwhere(universe == '#')
    
    pairs = get_unique_pairs(galaxies)
    
    # Calculate the distances
    distances = [galaxy_distance(a, b, [], [], 1) for a,b in pairs]
    return sum(distances)
    
def second(universe) -> int:
    # Collect the indices of the rows where no galaxies exist
    expanded_rows = []
    for i, row in enumerate(universe):
        if np.all(row == '.'):
            expanded_rows.append(i)
    
    # Collect the indices of the columns where no galaxies exist
    expanded_cols = []
    for j, col in enumerate(universe.T):
        if np.all(col == '.'):
            expanded_cols.append(j)

    # Find the galaxies and their (row, column) coordinates
    galaxies = np.argwhere(universe == '#')

    # Create unique pairs (upper-triangle only)
    pairs = get_unique_pairs(galaxies)
    
    # Calculate the distances
    distances = [galaxy_distance(a, b, expanded_rows, expanded_cols, 1_000_000-1) for a,b in pairs]
    return sum(distances)
    
    
if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=11, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
