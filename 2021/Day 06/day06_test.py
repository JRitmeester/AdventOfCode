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
import day06 as day

from aoc_util.helpers import load_input_data


@pytest.fixture
def preprocessed_input():
    input = load_input_data(file.parent / "example_input.txt", day=6, year=2021)
    return day.preprocess_input(input)


def test_preprocess_input(preprocessed_input):
    assert preprocessed_input == {1: 1, 2: 1, 3: 2, 4: 1}


def test_evolve(preprocessed_input):
    evolved = day.evolve(preprocessed_input, days=1)
    evolved_stripped = {
        days: count for days, count in evolved.items() if 0 <= days <= 3
    }
    print(evolved_stripped)
    assert evolved_stripped == {0: 1, 1: 1, 2: 2, 3: 1}


def test_first(preprocessed_input):
    result = day.first(preprocessed_input)
    assert result == 5934


def test_second(preprocessed_input):
    result = day.second(preprocessed_input)
    assert result == 26984457539


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
