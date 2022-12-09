import sys
from pathlib import Path
from ast import literal_eval

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


@print_timing
def first(lines) -> int:
    rawLen = sum(len(line) for line in lines)
    evalLen = sum(len(literal_eval(line)) for line in lines if len(line.strip()) > 0)
    return rawLen - evalLen


@print_timing
def second(lines) -> int:
    rawLen = sum(len(line) for line in lines)
    quotedLen = sum(len('"' + line.replace("\\", "\\\\").replace('"', '\\"') + '"')
                    for line in lines if len(line) > 0)
    return quotedLen - rawLen



if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=8, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
