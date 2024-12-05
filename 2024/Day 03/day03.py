from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import re


def get_multiplications(memory: str):
    hits = re.findall(r"(mul\(\d+,\d+\))", memory)
    sum = 0
    for hit in hits:
        factors = re.findall("\d+", hit)
        product = int(factors[0]) * int(factors[1])
        sum += product

    return sum


def preprocess_input(input_text: str):
    memory = input_text.replace("\n", "")
    return memory


def first(memory: str) -> int:
    return get_multiplications(memory)


def second(memory: str) -> int:
    total = 0

    hits = re.findall(r"^(.*?)don't\(\)|do\(\)(.*?)don't\(\)|do\(\)(.*)", memory)
    substrings = []
    for hit in hits:
        for h in hit:
            if h != "":
                substrings.append(h)
    total = get_multiplications("".join(substrings))
    return total


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=3, year=2024)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))  # 28880637 too low
