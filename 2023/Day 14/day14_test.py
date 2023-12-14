import os
import sys
from pathlib import Path
import numpy as np
import pytest
from pprint import pprint

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name == "Advent of Code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())
import day14 as day

from aoc_util.helpers import load_input_data


@pytest.fixture
def preprocessed_input():
    input = load_input_data(
        file.parent / "example_input.txt", day=14, year=2023
    )
    return day.preprocess_input(input)

def test_move_north(preprocessed_input):
    intended_outcome = day.preprocess_input((file.parent / "move_once.txt").read_text())
    after_move = day.move_platform(preprocessed_input, "up")
    assert np.array_equal(intended_outcome, after_move)

def test_cycles(preprocessed_input):
    intended_outcome_1 = day.preprocess_input((file.parent / "post_one_cycle.txt").read_text())
    intended_outcome_2 = day.preprocess_input((file.parent / "post_two_cycles.txt").read_text())
    intended_outcome_3 = day.preprocess_input((file.parent / "post_three_cycles.txt").read_text())

    post_one_cycle = day.do_cycle(preprocessed_input)
    post_two_cycles = day.do_cycle(post_one_cycle.copy())
    post_three_cycles = day.do_cycle(post_two_cycles.copy())

    assert np.sum(intended_outcome_1 != post_one_cycle) == 0
    assert np.sum(intended_outcome_2 != post_two_cycles) == 0
    assert np.sum(intended_outcome_3 != post_three_cycles) == 0

def test_first(preprocessed_input):
    result = day.first(preprocessed_input)
    assert result == 136


def test_second(preprocessed_input):
    result = day.second(preprocessed_input)
    assert result == 64


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
