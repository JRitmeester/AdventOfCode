from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
from itertools import combinations


def preprocess_input(input_text: str):
    """Parse input: each line is 'x,y' coordinates of a red tile."""
    lines = input_text.splitlines()
    return [tuple(map(int, line.split(","))) for line in lines]


def first(red_tiles) -> int:
    """Part 1: Find largest rectangle with any two red tiles as opposite corners."""
    max_area = 0
    best_pair = None

    for tile1, tile2 in combinations(red_tiles, 2):
        width = abs(tile2[0] - tile1[0]) + 1
        height = abs(tile2[1] - tile1[1]) + 1
        area = width * height

        if area > max_area:
            max_area = area
            best_pair = (tile1, tile2)

    return max_area


def fill_polygon(vertices, height, width):
    """Fill a rectilinear polygon: draw boundary + scanline fill interior."""
    mask = np.zeros((height, width), dtype=np.uint8)
    n = len(vertices)

    # Draw boundary
    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        if y1 == y2:
            mask[y1, min(x1, x2) : max(x1, x2) + 1] = 1
        else:
            mask[min(y1, y2) : max(y1, y2) + 1, x1] = 1

    # Fill interior with scanline
    for y in range(height):
        crossings = []
        for i in range(n):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % n]
            if y1 != y2 and ((y1 < y <= y2) or (y2 < y <= y1)):
                crossings.append(x1)
        crossings.sort()
        for j in range(0, len(crossings) - 1, 2):
            mask[y, crossings[j] : crossings[j + 1] + 1] = 1

    return mask


def second(red_tiles) -> int:
    """Part 2: Find largest rectangle with red corners inside the polygon."""
    if len(red_tiles) < 2:
        return 0

    # Coordinate compression
    unique_x = sorted(set(t[0] for t in red_tiles))
    unique_y = sorted(set(t[1] for t in red_tiles))
    x_idx = {x: i for i, x in enumerate(unique_x)}
    y_idx = {y: i for i, y in enumerate(unique_y)}

    # Create filled polygon mask
    vertices = [(x_idx[x], y_idx[y]) for x, y in red_tiles]
    mask = fill_polygon(vertices, len(unique_y), len(unique_x))

    # Group red tiles by row
    by_row = {}
    for x, y in red_tiles:
        by_row.setdefault(y_idx[y], []).append(x_idx[x])

    # Find largest valid rectangle
    max_area = 0
    rows = sorted(by_row)

    for i, r1 in enumerate(rows):
        for r2 in rows[i:]:
            valid = np.all(mask[r1 : r2 + 1, :], axis=0)

            for c1 in by_row[r1]:
                for c2 in by_row[r2]:
                    lo, hi = min(c1, c2), max(c1, c2)

                    if valid[lo : hi + 1].all():
                        w = unique_x[hi] - unique_x[lo] + 1
                        h = unique_y[r2] - unique_y[r1] + 1
                        max_area = max(max_area, w * h)

    return max_area


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=9, year=2025)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
