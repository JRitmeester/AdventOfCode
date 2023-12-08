from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from pprint import pprint

def preprocess_input(input_text: str):
    lines = input_text.splitlines()
    instructions = lines[0]
    nodes = lines[2:]

    map = {}
    for node in nodes:
        locations = re.findall('[A-Z0-9]{3}', node)
        map[locations[0]] = {'L': locations[1], 'R': locations[2]}
    return instructions, map

def least_common_multiple(ints: list[int]) -> list[int]:
    return np.lcm.reduce(ints)

def first(input_data) -> int:
    instructions, map = input_data

    position = 'AAA'
    steps_taken = 0
    instruction_count = 0
    while not position == 'ZZZ':
        position = map.get(position).get(instructions[instruction_count])
        steps_taken += 1
        instruction_count = (instruction_count + 1) % len(instructions)
    
    return steps_taken



def second(input_data) -> int:
    # Apparently the end node is one away from the starting node, so a full loop is also the distance to the end.
    # This is a massive assumption, that is not explicitly stated in the challenge.
    # But this does allow you to calculate the distance for each path individually, and find the least common multiple
    # of all lengths, without having to traverse the maze indefinitely (~10^12 steps)

    instructions, map = input_data
    positions = [node for node in map.keys() if node.endswith('A')]
    
    # Find the distance travelled for each starting node individually.
    loop_lengths = []
    for position in positions:
        steps_taken = 0
        instruction_count = 0
        while not position[2] == 'Z':
            position = map.get(position).get(instructions[instruction_count])
            steps_taken += 1
            instruction_count = (instruction_count + 1) % len(instructions)
            
        loop_lengths.append(steps_taken)
    
    return least_common_multiple(loop_lengths)
    

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=8, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
