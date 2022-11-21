import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint
from scipy.ndimage.morphology import binary_erosion as erode
from scipy.ndimage.morphology import binary_dilation as dilate
import imageio


def fold(paper: np.ndarray, axis: str, value: int):
    if axis == "y":
        h = paper.shape[0]
        if value >= h // 2:
            folded = np.flipud(paper[value + 1 :, :])
            paper = paper[:value, :]
            paper[-value:, :] += folded
        else:
            folded = np.flipud(paper[:value, :])
            paper = paper[value:, :]
            paper[value + 1 :, :] += folded

    elif axis == "x":
        w = paper.shape[1]

        if value >= w // 2:
            folded = np.fliplr(paper[:, value + 1 :])
            paper = paper[:, :value]
            paper[:, -value:] += folded

        else:
            folded = np.fliplr(paper[:, :value])
            paper = paper[:, value:]
            paper[:, value + 1 :] += folded

    paper = paper >= 1
    return paper


def main():
    input_raw = (Path(__file__).parent / "input.txt").read_text()
    dots, folds = input_raw.split("\n\n")

    dots = [dot.split(",") for dot in dots.split("\n")]
    dots = [(int(x), int(y)) for x, y in dots]

    folds = [(instruction[11], instruction[13:]) for instruction in folds.split("\n")]
    max_x = (max([int(dot[0]) for dot in dots])) + 1
    max_y = (max([int(dot[1]) for dot in dots])) + 1

    paper = np.zeros((max_y, max_x), dtype=np.int)
    for x, y in dots:
        paper[y, x] = 1

    for i, (axis, amount) in enumerate(folds):
        paper = fold(paper, axis, int(amount))

    plt.figure()
    plt.imshow(~paper)
    plt.gray()
    plt.show()


if __name__ == "__main__":
    main()
