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
from aoc_util.helpers import load_input_data

re_num_groups = re.compile(
    r"((\d)\2*)"
)  # Finds all the identical first numbers, e.g. (111, 2, 33, 2) in 1112332


def look_and_say(number: int, times: int):

    # Solution was originally my own, but modified it to this implementation, where re.sub takes in a callable
    # to achieve the desired speedup. (from https://www.reddit.com/r/adventofcode/comments/3w6h3m/comment/cxtsjx9/)
    def replace(match_obj):
        s = match_obj.group(1)
        return str(len(s)) + s[0]

    for _ in range(times):
        number = re_num_groups.sub(replace, number)

    return number


def preprocess_input(input_text: str):
    return input_text


def first(number) -> int:
    return len(look_and_say(number, 40))


def second(number) -> int:
    return len(look_and_say(number, 50))


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=10, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
