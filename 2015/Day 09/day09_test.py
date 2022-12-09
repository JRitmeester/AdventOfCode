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


@pytest.fixture
def preprocessed_input():
    input = load_input_data(
        file.parent / "example_input.txt", day=9, year=2015
    )
    return day.preprocess_input(input)


def test_first(preprocessed_input):
    result = day.first(preprocessed_input)
    assert result == 605


def test_second(preprocessed_input):
    result = day.second(preprocessed_input)
    assert result == None


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
