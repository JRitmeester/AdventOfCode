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


class Submarine:
    def __init__(self, use_aim: bool):
        self.pos = 0
        self.depth = 0
        self.aim = 0
        self.use_aim = use_aim

    def forward(self, x):
        self.pos += x
        if self.use_aim:
            self.depth += self.aim * x

    def up(self, x):
        if self.use_aim:
            self.aim -= x
        else:
            self.depth -= x

    def down(self, x):
        self.up(-x)

    def parse_instructions(self, instructions):
        for line in instructions:
            command, amount = line.split(" ")

            # Not very clean, but cooler than if statements.
            getattr(self, command)(int(amount))


def preprocess_input(input_text: str):
    return input_text.split("\n")


def first(input) -> int:
    sub = Submarine(use_aim=False)
    sub.parse_instructions(instructions=input)
    return sub.pos * sub.depth


def second(input) -> int | float:
    sub = Submarine(use_aim=True)
    sub.parse_instructions(instructions=input)
    return sub.pos * sub.depth


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=1, year=2021)
    input_ = preprocess_input(original_input)
    print("The answer to part 1 is:", first(input_))
    print("The answer to part 2 is:", second(input_))
