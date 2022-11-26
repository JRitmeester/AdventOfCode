import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data


def fold(paper: np.ndarray, axis: str, value: int):
    if axis == "y":
        h = paper.shape[0]
        if value >= h // 2:
            folded = np.fliplr(paper[value :, :])
            paper = paper[: value+1, :]
            paper[-value:, :] += folded
        else:
            folded = np.fliplr(paper[:value, :])
            paper = paper[value:, :]
            paper[value + 1 :, :] += folded

    elif axis == "x":
        w = paper.shape[1]

        if value >= w // 2:
            folded = np.flipud(paper[:, value + 1 :])
            paper = paper[:, :value]
            paper[:, -value:] += folded

        else:
            folded = np.flipud(paper[:, :value])
            paper = paper[:, value:]
            paper[:, value + 1 :] += folded

    paper = paper >= 1
    return paper


def preprocess_input(input_text: str):
    dots, folds = input_text.split("\n\n")
    dots = [dot.split(",") for dot in dots.split("\n")]
    dots = [(int(x), int(y)) for x, y in dots]
    folds = [(instruction[11], instruction[13:]) for instruction in folds.split("\n")]
    return dots, folds


def apply_folds(paper: np.array, folds: list[tuple]) -> np.array:
    for _, (axis, amount) in enumerate(folds):
        paper = fold(paper, axis, int(amount))
    return paper


def construct_paper(dots: list[tuple]) -> np.ndarray:
    max_x = (max([int(dot[0]) for dot in dots])) + 1
    max_y = (max([int(dot[1]) for dot in dots])) + 1
    paper = np.zeros((max_y, max_x), dtype=int)
    for x, y in dots:
        paper[y, x] = 1
    return paper


def first(input) -> int:
    dots, folds = input
    paper = construct_paper(dots)
    paper = apply_folds(paper, folds[0:1])
    return np.sum(paper)


def second(input) -> int:
    dots, folds = input
    paper = construct_paper(dots)
    paper = apply_folds(paper, folds)
    plt.figure()
    plt.imshow(~paper)
    plt.gray()
    plt.show()


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=13, year=2021)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
