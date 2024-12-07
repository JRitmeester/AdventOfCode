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
import day07 as day

from aoc_util.helpers import load_input_data


@pytest.fixture(
    params=[("example_input.txt", "first"), ("example_input_2.txt", "second")]
)
def preprocessed_input(request):
    input_file_name, part = request.param
    if not (file.parent / "example_input_2.txt").exists():
        input_file_name = "example_input.txt"

    input = load_input_data(file.parent / input_file_name, day=7, year=2024)
    return day.preprocess_input(input), part


def test_concatenate():
    assert day.concatentate(123, 456) == 123456


def test_solution(preprocessed_input):
    data, part = preprocessed_input
    if part == "first":
        result = day.first(data)
        assert result == 3749
    else:
        result = day.second(data)
        assert result == 11387


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
