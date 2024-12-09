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


@pytest.fixture(
    params=[("example_input.txt", "first"), ("example_input_2.txt", "second")]
)
def preprocessed_input(request):
    input_file_name, part = request.param
    if not (file.parent / "example_input_2.txt").exists():
        input_file_name = "example_input.txt"

    input = load_input_data(file.parent / input_file_name, day=9, year=2024)
    return day.preprocess_input(input), part


def test_sort_disk():
    assert (
        day.sort_disk("00...111...2...333.44.5555.6666.777.888899")
        == "0099811188827773336446555566"
    )


def test_expand_disk():
    assert day.expand_disk("233313312141413140251") == [
        "0",
        "0",
        ".",
        ".",
        ".",
        "1",
        "1",
        "1",
        ".",
        ".",
        ".",
        "2",
        ".",
        ".",
        ".",
        "3",
        "3",
        "3",
        ".",
        "4",
        "4",
        ".",
        "5",
        "5",
        "5",
        "5",
        ".",
        "6",
        "6",
        "6",
        "6",
        ".",
        "7",
        "7",
        "7",
        ".",
        "8",
        "8",
        "8",
        "8",
        "9",
        "9",
        ".",
        ".",
        ".",
        ".",
        ".",
        "10",
    ]


def test_solution(preprocessed_input):
    data, part = preprocessed_input
    if part == "first":
        result = day.first(data)
        assert result == 2132
    else:
        result = day.second(data)
        assert result == 2858


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
