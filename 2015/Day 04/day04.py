import sys
from hashlib import md5
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


@print_timing
def first(input_data) -> int:
    i = 0
    while True:
        string = input_data + str(i)
        hash = md5(bytes(string, encoding="ascii")).hexdigest()
        if hash[:5] == "00000":
            return i
        i += 1


@print_timing
def second(input_data) -> int:
    i = 0
    while True:
        string = input_data + str(i)
        hash = md5(bytes(string, encoding="ascii")).hexdigest()
        if hash[:6] == "000000":
            return i
        i += 1


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=4, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
