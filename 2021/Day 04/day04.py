import re
import sys
from pathlib import Path

import numpy as np

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data


class Card:

    """
    Class to contain the bingo cards, along with information on whether any positions has been called, and
    a function to check newly called numbers and check for bingo.
    """

    def __init__(self, card_numbers):

        # Thanks to Jessseee for this parsing solution.
        card_numbers = [
            [int(num) for num in re.findall(".. ?", line)]
            for line in card_numbers.split("\n")
        ]
        self.card = np.array(card_numbers).astype(int)
        self.mask = np.zeros_like(self.card)
        self.has_bingo = False

    def check_number(self, num):
        self.mask[self.card == num] = 1
        for i in range(5):
            if np.sum(self.mask[i, :]) == 5 or np.sum(self.mask[:, i]) == 5:
                self.has_bingo = True


def calculate_card_score(card: Card, last_number: int) -> int:
    """
    Return the score as described by the challenge: the sum of all the unmarked numbers on the card,
    multiplied by the last called number.

    Args:
        card (Card): the score card
        last_number (int): the last bingo number that was called

    Returns:
        int: the card's score
    """
    return np.sum(np.multiply(1 - card.mask, card.card)) * last_number


def preprocess_input(original_input: str) -> tuple[np.ndarray, list[Card]]:
    """
    Split the raw text format into the bingo numbers and 100 separate bingo cards.

    Args:
        original_input (str): input data from the challenge
        list (list[Card]): list of bingo card objects

    Returns:
        tuple(np.ndarray, list[Card]): the bingo numbers and the bingo cards
    """
    sequence, *cards_raw = original_input.split("\n\n")
    sequence = np.array(sequence.split(","), dtype=int)
    cards = [Card(card_raw) for card_raw in cards_raw]
    return sequence, cards


def first(sequence: np.ndarray, cards: list[Card]) -> int:
    """
    For the first card to have bingo, calculate the sum of all unmarked numbers,
    multiplied by the last called number.

    Args:
        sequence (np.ndarray): The called bingo numbers
        cards (list[Card]): The bingo cards

    Returns:
        int: The score of the first winning bingo card.
    """
    for number in sequence:
        for card in cards:
            card.check_number(number)
            if card.has_bingo:
                return calculate_card_score(card, number)


def second(sequence: np.ndarray, cards: list[Card]) -> int:
    """
    Find which bingo card has bingo the LAST, and return its score.


    Args:
        sequence (np.ndarray): The called bingo numbers
        cards (list[Card]): The bingo cards

    Returns:
        int: The score of the last winning bingo card.
    """
    store_card = None
    store_number = None

    for number in sequence:
        for card in cards:
            if card.has_bingo:
                continue
            card.check_number(number)
            if card.has_bingo:
                store_card = card
                store_number = number
    return calculate_card_score(store_card, store_number)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=4, year=2021)
    sequence, cards = preprocess_input(original_input)
    print("The answer to part 1 is:", first(sequence, cards))
    print("The answer to part 2 is:", second(sequence, cards))
