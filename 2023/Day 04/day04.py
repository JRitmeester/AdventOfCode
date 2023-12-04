from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from pprint import pprint

def preprocess_input(input_text: str):
    lines = input_text.split('\n')
    scratchcards = []
    for line in lines:
        _, numbers = line.split(': ')
        winning_numbers, game_numbers = numbers.split('|')
        winning_numbers = [int(x) for x in re.findall('\d+', winning_numbers)]
        game_numbers = [int(x) for x in re.findall('\d+', game_numbers)]
        scratchcards.append((winning_numbers, game_numbers))
    return scratchcards


def first(scratchcards) -> int:
    print(scratchcards)
    scores = []
    for winning_numbers, game_numbers in scratchcards:
        matches = np.sum([winning_number in game_numbers for winning_number in winning_numbers])
        print(matches)
        if matches > 0:
            scores.append(2**(matches-1))
    return np.sum(scores)



def second(scratchcards) -> int:
    number_of_copies = {idx: 1 for idx in range(len(scratchcards))}
    for i, (winning_numbers, game_numbers) in enumerate(scratchcards):
        matches = np.sum([winning_number in game_numbers for winning_number in winning_numbers])
        print(i, matches)
        for j in range(matches):
            number_of_copies[i+j+1] += number_of_copies[i]
        pprint(number_of_copies)
    
    return sum(list(number_of_copies.values()))
    

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=4, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
