import os
import sys
from pathlib import Path

import pytest

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name == "Advent of Code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())
import day09 as day

from aoc_util.helpers import load_input_data


def test_first():
    preprocessed_input = load_input_data(
        file.parent / "example_input_1.txt", day=9, year=2022
    )
    result = day.first(day.preprocess_input(preprocessed_input))
    assert result == 13


def test_second():
    preprocessed_input = load_input_data(
        file.parent / "example_input_2.txt", day=9, year=2022
    )
    result = day.second(day.preprocess_input(preprocessed_input))
    assert result == 36


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
