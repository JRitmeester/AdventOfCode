import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint
import re


def turns_before_bingo(card, sequence):
    mask = np.zeros_like(card)
    for i, num in enumerate(sequence):
        loc = np.argwhere(np.array(card) == num)
        if len(loc) > 0:
            y, x = loc[0]
            mask[y, x] = 1
            if np.sum(mask[y, :]) == 5 or np.sum(mask[:, x]) == 5:
                return i, num, mask


def find_score(cards, sequence, goal):
    store_turns = 100 if goal == "win" else 0
    store_card = None
    store_number = None
    store_mask = None

    for card in cards:
        turns, last, mask = turns_before_bingo(card, sequence)
        if (goal == "win" and turns < store_turns) or (
            goal == "lose" and turns > store_turns
        ):
            store_card = card
            store_turns = turns
            store_number = last
            store_mask = mask

    return np.sum(np.multiply(store_card, 1 - store_mask)) * store_number


def main():
    input_raw = (Path(__file__).parent / "input.txt").read_text()
    # print(input_raw)
    split_input = input_raw[:-1].split("\n\n")

    # Thanks to Jessseee for this parsing solution.
    sequence = [int(num) for num in split_input[0].split(",")]
    cards = [
        [[int(num) for num in re.findall(".. ?", line)] for line in board.split("\n")]
        for board in split_input[1:]
    ]

    print("Answer part 1:", find_score(cards, sequence, goal="win"))
    print("Answer part 2:", find_score(cards, sequence, goal="lose"))


if __name__ == "__main__":
    main()
