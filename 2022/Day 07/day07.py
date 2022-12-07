import os
import re
import shutil
import sys
from pathlib import Path
from pprint import pprint

import numpy as np
import pandas as pd

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data, print_timing

root = Path(__file__).parent / "root"


@print_timing
def preprocess_input(input_text: str):
    lines = input_text.split("\n")
    create_file_tree(lines[1:])  # Discard the '$ cd /' line.


def create_file_tree(log_lines):
    cwd = root
    if cwd.exists():
        shutil.rmtree(cwd)
    cwd.mkdir()

    re_cd = re.compile("^\$ cd ([a-z\./]+)$")
    re_dir = re.compile("^dir ([a-z.]+)$")
    re_file = re.compile("^([0-9]+) [a-z.]+$")
    re_ls = re.compile("^\$ ls$")

    for i, line in enumerate(log_lines):
        cd = re_cd.match(line)
        if cd:  # If a cd command is encountered, move the cwd to the correct position.
            to_dir = cd.group(1)
            if to_dir == "..":  # Move up one directory.
                cwd = cwd.parent
            else:  # Go into the child by setting the cwd to it.
                cwd = cwd / to_dir

        else:
            dir = re_dir.match(line)
            if dir:  # If a dir prompt is encountered, create these folders if needed.
                dir_name = dir.group(1)
                (cwd / dir_name).mkdir(exist_ok=True)  # Create the child directory.

            else:
                file_size = re_file.match(line)
                if (
                    file_size
                ):  # If a file description is encountered, create a text file with the file size in it.
                    size, name = line.split(" ")
                    (cwd / name).write_text(size)

                else:
                    ls = re_ls.match(line)
                    if ls:
                        continue


def get_dir_size(path="."):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += int(Path(entry).read_text())
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total


def get_all_dir_sizes():
    dir_sizes = {
        dir: get_dir_size(dir)
        for dir in [path for path in root.rglob("*") if path.is_dir()]
    }
    return dir_sizes


@print_timing
def first() -> int:
    all_dir_sizes = get_all_dir_sizes()
    return sum(dir_size for dir_size in all_dir_sizes.values() if dir_size <= 100000)


@print_timing
def second() -> int:
    all_dir_sizes = pd.Series(get_all_dir_sizes())
    root_size = get_dir_size(root)
    free_space = 70_000_000 - root_size
    required_space = 30_000_000 - free_space
    dir_size_diff = all_dir_sizes - required_space
    closest_dir = dir_size_diff[dir_size_diff >= 0].idxmin()
    return all_dir_sizes[closest_dir]


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=7, year=2022)
    preprocess_input(original_input)

    print("The answer to part 1 is:", first())
    print("The answer to part 2 is:", second())
