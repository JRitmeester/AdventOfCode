import pytest
import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).parent.parent.parent))
from aoc_util.helpers import load_input_data
import day05
import numpy as np

cwd = Path(__file__).parent


@pytest.fixture
def input_text():
    input_ = load_input_data(cwd / "example_input.txt", day=5, year=2021)
    return day05.preprocess_input(input_)


def test_create_map_vh(input_text: str):
    map_vh = day05.create_map(input_text, include_diagonal=False, size=(10, 10))
    expected_map_vh = """.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111...."""
    expected_map_vh = np.array([list(char) for char in expected_map_vh.split("\n")])
    expected_map_vh[expected_map_vh == "."] = 0
    expected_map_vh = expected_map_vh.astype(int)
    assert np.array_equal(map_vh, expected_map_vh)


def test_create_map_diag(input_text):
    map_diag = day05.create_map(input_text, include_diagonal=True, size=(10, 10))
    expected_map_diag = """1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111...."""
    expected_map_diag = np.array([list(char) for char in expected_map_diag.split("\n")])
    expected_map_diag[expected_map_diag == "."] = 0
    expected_map_diag = expected_map_diag.astype(int)
    assert np.array_equal(map_diag, expected_map_diag)


def test_first(input_text):
    print(input_text)
    score = day05.first(input_text)
    assert score == 5


def test_second(input_text):
    score = day05.second(input_text)
    assert score == 12


if __name__ == "__main__":
    os.chdir(cwd)
    os.system("pytest . -s")
