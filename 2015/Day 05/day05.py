import re
import string
import sys
from pathlib import Path

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

"""
import string
import re

include = [x*2 for x in string.ascii_lowercase ]
exclude = ['ab','cd','pq','xy'] 

def meets_req_1(line: str) -> bool:
	if not any([x in line for x in exclude]) and any([x in line for x in include]):
		remaining_str = re.sub('ab|cd|pq|xy', '', line)
		vowels = sum([x in 'aeoui' for x in remaining_str])
		if vowels >= 3:
			return True
	return False

print(sum([meets_req_1(line) for line in lines]))"""


def meets_req_1(line: str) -> bool:
    include = [x * 2 for x in string.ascii_lowercase]
    exclude = ["ab", "cd", "pq", "xy"]

    if not any([x in line for x in exclude]) and any([x in line for x in include]):
        remaining_str = re.sub("ab|cd|pq|xy", "", line)
        vowels = sum([x in "aeoui" for x in remaining_str])
        if vowels >= 3:
            return True
    return False


def meets_req_2(line: str) -> bool:
    rule1= re.compile(r"^.*(..).*\1.*$")
    rule2= re.compile(r"^.*(.).\1.*$")
    return bool(rule1.match(line)) and bool(rule2.match(line))


@print_timing
def preprocess_input(input_text: str):
    return input_text.split("\n")


@print_timing
def first(lines) -> int:
    return sum([meets_req_1(line) for line in lines])


@print_timing
def second(lines) -> int:
    return sum([meets_req_2(line) for line in lines])


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=5, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
