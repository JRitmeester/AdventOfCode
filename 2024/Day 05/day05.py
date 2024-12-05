from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint


def check_update_order(rules: list[str], update: list[str]) -> int | None:
    for i, first in enumerate(update):
        for second in update[i + 1 :]:
            rule = f"{first}|{second}"
            if not rule in rules:
                return None

    middle_index = len(update) // 2
    middle_page = update[middle_index]
    return middle_page


def fix_update_order(rules: list[str], update: list[str]) -> int:
    # Filter only the rules that are relevant to this update, i.e. only rules where both X and Y are present in the update page numbers.
    relevant_rules = []
    for i, first in enumerate(update):
        for second in update[i + 1 :]:
            rule = f"{first}|{second}"
            reverse_rule = f"{second}|{first}"
            if rule in rules:
                relevant_rules.append(rule)
            if reverse_rule in rules:
                relevant_rules.append(reverse_rule)

    # Count how many rules there are that start with page X, and sort them according to this count.
    X_counts = {}
    for rule in relevant_rules:
        X, Y = rule.split("|")
        if X in X_counts:
            X_counts[X] += 1
        else:
            X_counts[X] = 1

        # The last page in the rule won't occur as X, so set it 0 using Y.
        if not Y in X_counts:
            X_counts[Y] = 0

    # Sort the dict by value
    X_counts = dict(sorted(X_counts.items(), key=lambda item: item[1], reverse=True))
    corrected_update = [int(x) for x in X_counts.keys()]
    middle_index = len(corrected_update) // 2
    middle_page = corrected_update[middle_index]
    return middle_page


def preprocess_input(input_text: str):
    rules, updates = input_text.split("\n\n")
    rules = rules.split()
    updates = [tuple(line.split(",")) for line in updates.split()]
    return rules, updates


def first(rules: list[str], updates: list[str]) -> int:
    middle_pages = []
    for update in updates:
        middle_pages.append(check_update_order(rules, update))
    return sum([int(x) for x in middle_pages if x is not None])


def second(rules: list[str], updates: list[str]) -> int:
    incorrect_updates = []
    for update in updates:
        middle_page = check_update_order(rules, update)
        if middle_page is None:
            incorrect_updates.append(update)

    middle_pages = []
    for update in incorrect_updates:
        middle_pages.append(fix_update_order(rules, update))

    return sum([int(x) for x in middle_pages])


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=5, year=2024)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(*preprocessed_input))
    print("The answer to part 2 is:", second(*preprocessed_input))
