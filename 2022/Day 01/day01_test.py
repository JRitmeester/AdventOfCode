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
if REPO_ROOT:
    sys.path.append(REPO_ROOT.as_posix())
import day01 as day

from aoc_util.helpers import load_input_data


@pytest.fixture
def preprocessed_input():
    input = load_input_data(file.parent / "example_input.txt", day=1, year=2022)
    return day.preprocess_input(input)


def test_preprocessed_input(preprocessed_input):
    assert preprocessed_input == [6000, 4000, 11000, 24000, 10000]


def test_first(preprocessed_input):
    result = day.first(preprocessed_input)
    assert result == 24000


def test_second(preprocessed_input):
    result = day.second(preprocessed_input)
    assert result == 45000


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
