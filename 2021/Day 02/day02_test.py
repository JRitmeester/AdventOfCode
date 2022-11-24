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
import day02 as day

from aoc_util.helpers import load_input_data


@pytest.fixture
def input_text():
    input = load_input_data(file.parent / "example_input.txt", day={1}, year={2})
    return day.preprocess_input(input)


def test_first(input_text):
    result = day.first(input_text)
    assert result == 150


def test_second(input_text):
    result = day.second(input_text)
    assert result == 900


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
