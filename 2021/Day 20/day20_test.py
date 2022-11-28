import os
import sys
from pathlib import Path

import numpy as np
import pytest

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name == "Advent of Code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())
import day20 as day

from aoc_util.helpers import load_input_data


@pytest.fixture
def preprocessed_input():
    input = load_input_data(file.parent / "example_input.txt", day=20, year=2021)
    return day.preprocess_input(input, shape=(15, 15))


def test_preprocessed_input(preprocessed_input):
    example_sequence = "..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#"
    example_sequence = np.array(list(example_sequence)) == "#"
    assert np.array_equal(preprocessed_input[0], example_sequence)

    example_image = """...............
...............
...............
...............
...............
.....#..#......
.....#.........
.....##..#.....
.......#.......
.......###.....
...............
...............
...............
...............
..............."""
    example_image_rows = example_image.split("\n")
    example_image_oneline = "".join(example_image_rows)
    example_image_arr = np.array(list(example_image_oneline)).reshape((15, 15))
    example_image_converted = example_image_arr == "#"
    assert np.sum(example_image_converted) == 10


def test_retrieve_pixels(preprocessed_input):
    sequence, image = preprocessed_input
    test_image = ""


def test_first(preprocessed_input):
    result = day.first(preprocessed_input)
    assert result == 35


def test_second(preprocessed_input):
    result = day.second(preprocessed_input)
    assert result == None


if __name__ == "__main__":
    os.system(f'pytest "{file}" -s')
