from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from collections import Counter
from pprint import pprint

ORIGINAL_CARD_ORDER = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
NEW_CARD_ORDER = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]
TYPE_ORDER = ["5", "4", "FH", "3", "2P", "1P", "H"]


class Hand:
    def __init__(self, hand: str, bid: int, new_rules: bool):
        self.hand = hand
        self.adjusted_hand = hand
        self.bid = bid
        self.card_count = Counter(self.hand)
        self.jokers = self.card_count["J"]
        self.type = self._get_type(new_rules)
        self.new_rules = new_rules

    def _get_type(self, new_rules) -> (int, int):
        # TODO: what to do if J is the most common card
        most_common_card, most_common_card_count = self.card_count.most_common(1)[0]
        if new_rules:
            if most_common_card == "J":
                if most_common_card_count == 5:
                    hand = "AAAAA"
                else:
                    most_common_card, most_common_card_count = self.card_count.most_common(2)[1]
            hand = self.hand.replace("J", most_common_card)
            card_count = Counter(hand)
        else:
            hand = self.hand
            card_count = self.card_count

        most_common_card, most_common_card_count = card_count.most_common(1)[0]
        pairs = sum(
            [v == 2 for v in card_count.values()]
        )

        if most_common_card_count == 5:
            type_ = "5"
        elif most_common_card_count == 4:
            type_ = "4"
        elif most_common_card_count == 3:
            if pairs == 0:
                type_ = "3"
            elif pairs == 1:
                type_ = "FH"
        elif most_common_card_count == 2:
            if pairs == 2:
                type_ = "2P"
            elif pairs == 1:
                type_ = "1P"
        elif most_common_card_count == 1:
            type_ = "H"
        return type_

    
    def _tiebreaker(self, other):
        for own_card, other_card in zip(self.hand, other.hand):
            if own_card != other_card:
                if self.new_rules:
                    return NEW_CARD_ORDER.index(own_card) < NEW_CARD_ORDER.index(other_card)
                else:
                    return ORIGINAL_CARD_ORDER.index(own_card) < ORIGINAL_CARD_ORDER.index(other_card)
                    

    def __str__(self):
        return self.hand

    def __repr__(self):
        return f"{self.hand=} [{self.type=}, {self.bid=}]"

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


def create_hands(hands_and_bids, new_rules: bool):
    return [Hand(hand, int(bid), new_rules=new_rules) for hand, bid in hands_and_bids]


def preprocess_input(input_text: str):
    lines = input_text.splitlines()
    hands_and_bids = list(map(str.split, lines))
    return hands_and_bids


def first(hands_and_bids) -> int:
    hands = create_hands(hands_and_bids, new_rules=False)
    sorted_hands = sorted(hands)
    winnings = [i * hand.bid for i, hand in enumerate(sorted_hands, 1)]
    return np.sum(winnings)


def second(hands_and_bids) -> int:
    hands = create_hands(hands_and_bids, new_rules=True)
    sorted_hands = sorted(hands)
    pprint(sorted_hands)
    winnings = [i * hand.bid for i, hand in enumerate(sorted_hands, 1)]
    return np.sum(winnings)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=7, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
