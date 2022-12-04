import re
import sys
from pathlib import Path

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
    passwords = []
    lines = input_text.split("\n")
    for line in lines:
        min_n, max_n = re.findall("[0-9]+", line)  #
        char = re.findall("([a-z])(?=:)", line)[
            0
        ]  # Find a character that has a colon after it.
        password = list(
            re.findall("([a-z]*$)", line)[0]
        )  # Find all consecutive characters at the end of the string.
        passwords.append((int(min_n), int(max_n), char, password))
    return passwords


@print_timing
def first(password_info) -> int:
    return sum(
        min_n <= password.count(char) <= max_n
        for min_n, max_n, char, password in password_info
    )


@print_timing
def second(password_info) -> int:
    return sum(
        (password[pos_1 - 1] == char) ^ (password[pos_2 - 1] == char)
        for pos_1, pos_2, char, password in password_info
    )


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=2, year=2020)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
