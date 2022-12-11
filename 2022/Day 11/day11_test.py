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
import day11 as day

from aoc_util.helpers import load_input_data


@pytest.fixture
def preprocessed_input():
    input = load_input_data(file.parent / "example_input.txt", day=11, year=2022)
    return day.preprocess_input(input)


def test_monkey(preprocessed_input):
    test_monkey = preprocessed_input[0]
    assert test_monkey.id == 0
    assert test_monkey.items == [79, 98]
    assert test_monkey.operation(10) == 190
    assert test_monkey.test == 23
    assert test_monkey.true_id == 2
    assert test_monkey.false_id == 3


def test_single_round(preprocessed_input):
    monkeys = day.keep_away(preprocessed_input, 1, relief=True)
    assert monkeys[0].items == [20, 23, 27, 26]
    assert monkeys[1].items == [2080, 25, 167, 207, 401, 1046]
    assert monkeys[2].items == []
    assert monkeys[3].items == []


def test_first(preprocessed_input):
    result = day.first(preprocessed_input)
    assert result == 10_605


def test_second(preprocessed_input):
    result = day.second(preprocessed_input)
    assert result == 2_713_310_158


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
