from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import re
from itertools import permutations


def preprocess_input(input_text: str):
    pairings = {}
    guests = []
    for line in input_text.split("\n"):
        parts = line.split(" ")
        first = parts[0]
        guests.append(first)
        last = parts[-1][:-1]  # Remove period
        happiness = re.search("\d+", line).group(0)
        pairings[tuple([first, last])] = int(happiness) * (-1 if "lose" in line else 1)
    guests = list(set(guests))
    return guests, pairings


def calculate_happiness(pairings: dict, table: tuple) -> int:
    total_happiness = 0
    for i in range(1, len(table)):
        p1 = table[i - 1]
        p2 = table[i]
        total_happiness += pairings[(p1, p2)]
        total_happiness += pairings[(p2, p1)]
    total_happiness += pairings[(table[len(table) - 1], table[0])]
    total_happiness += pairings[(table[0], table[len(table) - 1])]
    return total_happiness


def first(guests, pairings) -> int:
    return max(
        calculate_happiness(pairings, table) for table in set(permutations(guests))
    )


def second(guests, pairings) -> int:
    for guest in guests:
        pairings[(guest, "Me")] = 0
        pairings[("Me", guest)] = 0
    guests.append("Me")
    print(guests)
    return max(
        calculate_happiness(pairings, table) for table in set(permutations(guests))
    )


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=13, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(*preprocessed_input))
    print("The answer to part 2 is:", second(*preprocessed_input))
