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
import day04 as day

from aoc_util.helpers import load_input_data


@pytest.fixture
def preprocessed_input_1():
    input = load_input_data(file.parent / "example_input_1.txt", day=4, year=2020)
    return day.preprocess_input(input)

@pytest.fixture
def preprocessed_input_2():
    input = load_input_data(file.parent / "example_input_2.txt", day=4, year=2020)
    return day.preprocess_input(input)

def test_first(preprocessed_input_1):
    result = day.first(preprocessed_input_1)
    assert result == 2


def test_second(preprocessed_input_2):
    result = day.second(preprocessed_input_2)
    assert result == 4


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
