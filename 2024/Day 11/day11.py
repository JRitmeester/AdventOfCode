from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *


def evolve_stone(stone: str) -> list[str]:
    if stone == "0":
        return ["1"]
    if len(stone) % 2 == 0:
        l = len(stone) // 2
        return [str(int(stone[:l])), str(int(stone[l:]))]
    else:
        return [str(int(stone) * 2024)]


def evolve_stones(counts: dict) -> dict:
    new_counts = {}
    for n, count in counts.items():
        resulting_stones = evolve_stone(n)
        for stone in resulting_stones:
            if stone not in new_counts:
                new_counts[stone] = 0
            new_counts[stone] += count
    return new_counts


def preprocess_input(input_text: str):
    return input_text.split()


@print_timing
def first(stones: list[str]) -> int:
    counts = {}
    for stone in stones:
        if stone not in counts:
            counts[stone] = 0
        counts[stone] += 1

    for _ in range(25):
        counts = evolve_stones(counts)

    return sum(counts.values())


@print_timing
def second(stones: list[str]) -> int:
    counts = {}
    for stone in stones:
        if stone not in counts:
            counts[stone] = 0
        counts[stone] += 1

    for _ in range(75):
        counts = evolve_stones(counts)

    return sum(counts.values())


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=11, year=2024)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
