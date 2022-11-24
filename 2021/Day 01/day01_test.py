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
import day01

from aoc_util.helpers import load_input_data


@pytest.fixture
def input_text():
    input_ = load_input_data(
        Path(__file__).parent / "example_input.txt", day=1, year=2021
    )
    return day01.preprocess_input(input_)


def test_first(input_text):
    assert day01.first(input_text) == 7


def test_second(input_text):
    assert day01.second(input_text) == 5


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
