from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter
from pprint import pprint

CARD_ORDER = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
TYPE_ORDER = ["5", "4", "FH", "3", "2P", "1P", "H"]

class Hand:

    def __init__(self, hand: str, bid: int):
        self.hand = hand
        self.bid = bid
        self.card_count = Counter(self.hand)
        self.type = self._get_type()


    def _get_type(self) -> (int, int):
        highest_n_same_cards = max(self.card_count.values())  # Get the highest number of same cards, e.g. AA234 --> 2
        pairs = sum([v == 2 for v in self.card_count.values()])  # Get the number of pairs, e.g. AA234 --> 1

        if highest_n_same_cards == 5:
            type_ = "5"
        elif highest_n_same_cards == 4:
            type_ = "4"
        elif highest_n_same_cards == 3:
            if pairs == 0:
                type_ = "3"
            elif pairs == 1:
                type_ = "FH"
        elif highest_n_same_cards == 2:
            if pairs == 2:
                type_ = "2P"
            elif pairs == 1:
                type_ = "1P"
        elif highest_n_same_cards == 1:
            type_ = "H"
        return type_
    

    def _tiebreaker(self, other):
        for own_card, other_card in zip(self.hand, other.hand):
            if own_card != other_card:
                return CARD_ORDER.index(own_card) < CARD_ORDER.index(other_card)

    def __str__(self):
        return self.hand
    
    def __repr__(self):
        return f"{self.hand=} [{self.type=}, {self.pairs=}, {self.bid=}]"
    
 
    def __gt__(self, other):
        if self.type == other.type:
            return self._tiebreaker(other)
        else:
            return TYPE_ORDER.index(self.type) < TYPE_ORDER.index(other.type)
            
    def __eq__(self, other) -> bool:
        """
        Abuse the equality operator to see if the types are the same, not if the hands are identical.
        """
        return self.type == other.type


def preprocess_input(input_text: str):
    lines = input_text.splitlines()
    hands_and_bids = list(map(str.split, lines))
    hands = [Hand(hand, int(bid)) for hand, bid in hands_and_bids]
    return hands


def first(hands) -> int:
    sorted_hands = sorted(hands)
    winnings = [i*hand.bid for i, hand in enumerate(sorted_hands, 1)]
    return np.sum(winnings)


def second(input_data) -> int:
    pass

if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=7, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
