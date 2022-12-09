import re
import sys
from pathlib import Path
from pprint import pprint

import numpy as np
import pandas as pd

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data, print_timing


@print_timing
def preprocess_input(input_text: str):
    return input_text.split("\n")


def to_bit_array(number: str) -> np.ndarray:
    bit_array = np.array(list(bin(int(number))[2:])).astype(int)
    bit_array = np.append(np.array([0] * (16 - len(bit_array))), bit_array)
    return bit_array

def run_simulation(lines: list[str], override_b: bool) -> int:
    calc = {}
    results = {}

    for command in lines:
        (ops, res) = command.split("->")
        calc[res.strip()] = ops.strip().split(" ")

    def calculate(name):
        if name.isnumeric():
            return int(name)

        if name not in results:
            if override_b and name == 'b':
                return 16076
            ops = calc[name]
            if len(ops) == 1:
                res = calculate(ops[0])
            else:
                op = ops[-2]
                if op == "AND":
                    res = calculate(ops[0]) & calculate(ops[2])
                elif op == "OR":
                    res = calculate(ops[0]) | calculate(ops[2])
                elif op == "NOT":
                    res = ~calculate(ops[1]) & 0xFFFF
                elif op == "RSHIFT":
                    res = calculate(ops[0]) >> calculate(ops[2])
                elif op == "LSHIFT":
                    res = calculate(ops[0]) << calculate(ops[2])
            results[name] = res
        return results[name]

    return calculate("a")
@print_timing
def first(lines) -> int:
    """
    Thanks to u/Tryneus (https://www.reddit.com/r/adventofcode/comments/3vr4m4/comment/cxpz4tq/)
    Got close but not close enough.
    """
    return run_simulation(lines, override_b=False)

@print_timing
def second(lines) -> int:
    return run_simulation(lines, override_b=True)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=7, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
