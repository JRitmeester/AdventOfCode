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


class Thingy:
    def __init__(self, unique_signal: str):
        """
        Numbers can be found by substracting the segments from eachother. For example the digit 7 - digit 1 leaves only
        one segment. Similarly, any digit - digit 8 leaves no segment.

        3 - 7 leaves 2 segments,
        2 - 7 leaves 3 segments,
        5 - 7 leaves 3 segments,
        Hence, if the digit's length is 5 and subtracting digit 7 leaves 2 segments, the digit was 3.

        2 - 4 leaves 3 segments,
        5 - 4 leaves 2 segments,
        Hence, if the digit's length is 5 and subtracting digit 4 leaves 3 segments, the digit was 2.
        Otherwise it was 5.

        0 - 7 leaves 3 segments,
        6 - 7 leaves 4 segments,
        9 - 7 leaves 3 segments,
        Hence, if the digit's length is 6 and subtracting digit 7 leaves 4 segments, the digit was 6.

        0 - 4 leaves 3 segments,
        9 - 4 leaves 2 segments,
        Hence, if the digit's length is 6 and substracting digit 4 leaves 3 segments, the digit was 0.
        Otherwise it was 9.

        """
        self.unique_signal = sorted(
            [set(x) for x in unique_signal.split(" ")], key=lambda x: len(x)
        )

        self.mapping = {num: None for num in range(10)}
        self[1] = self.get_signals_by_length(2)[0]
        self[7] = self.get_signals_by_length(3)[0]
        self[4] = self.get_signals_by_length(4)[0]
        self[8] = self.get_signals_by_length(7)[0]

        length_five = self.get_signals_by_length(5)
        self[3] = [x for x in length_five if len(x - self[7]) == 2][0]
        self[5] = [x for x in length_five if len(x - self[4]) == 2 and x != self[3]][0]
        self[2] = [x for x in length_five if x != self[3] and x != self[5]][0]

        length_six = self.get_signals_by_length(6)
        self[6] = [x for x in length_six if len(x - self[7]) == 4][0]
        self[9] = [x for x in length_six if len(x - self[4]) == 2 and x != self[6]][0]
        self[0] = [x for x in length_six if x != self[6] and x != self[9]][0]

        self.reverse_mapping = {
            tuple(sorted(val)): key for key, val in self.mapping.items()
        }

        # Debug: double check if all keys are unique.
        assert len(set([tuple(x) for x in self.reverse_mapping.keys()])) == 10

    def __getitem__(self, key):
        return self.mapping[key]

    def __setitem__(self, key, value):
        self.mapping[key] = value

    def translate(self, output_value):
        """
        Beefy one-liner: split the output value to obtain 4 sets of segments. Sort them and turn them into tuples,
        so that they can be used as keys in the mapping dictionary. Turn each result into a string so they can be
        concatenated, and turn the resulting 4 digit number into an integer. What could possibly go wrong?
        """
        return int(
            "".join(
                [
                    str(self.reverse_mapping[tuple(sorted(x))])
                    for x in output_value.split(" ")
                ]
            )
        )

    def get_signals_by_length(self, length: int):
        return [x for x in self.unique_signal if len(x) == length]


def preprocess_input(input_text: str):
    return [tuple(line.split(" | ")) for line in input_text.split("\n")]


def first(input) -> int:
    total = 0
    for unique_signal, output_value in input:
        digits = output_value.split(" ")
        for digit in digits:
            if len(digit) in [2, 3, 4, 7]:
                total += 1
    return total


def second(input) -> int:
    total = 0
    for i, (unique_signal, output_value) in enumerate(input):
        # output += Thingy(unique_signal).translate(output_value)
        thingy = Thingy(unique_signal)
        output = thingy.translate(output_value)
        total += output
    return total


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=8, year=2021)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
