import re
import string
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
    return input_text


def get_next_password(password):
    alphabet = string.ascii_lowercase
    consec_triplets = [
        "".join([alphabet[i], alphabet[i + 1], alphabet[i + 2]]) for i in range(24)
    ]
    find_pairs = re.compile(r"((\w)\2)")

    def increment(password):
        pass_to_num = [alphabet.index(char) for char in password]
        pass_to_num[-1] += 1
        for i in range(len(pass_to_num) - 1, 0, -1):
            if pass_to_num[i] >= 26:
                pass_to_num[i] -= 26
                pass_to_num[i - 1] += 1
        password = "".join([alphabet[i] for i in pass_to_num])
        return password

    while True:
        password = increment(password)
        if not any([triplet in password for triplet in consec_triplets]):
            continue
        if any([char in password for char in ["i", "o", "l"]]):
            continue
        if len(set(find_pairs.findall(password))) < 2:
            continue
        return password


def first(password) -> int:
    return get_next_password(password)


def second(password) -> int:
    return get_next_password(get_next_password(password))


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=11, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
