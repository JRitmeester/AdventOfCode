import heapq
import sys
from pathlib import Path

import numpy as np

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data


def dijkstra(cave):
    """
    Credits to github.com/michaeljgallagher for this implementation.
    """
    h, w = cave.shape

    costs = {}

    # Store the cost and the two coordinates on a heap (used as priority queue).
    heap = [(0, 0, 0)]

    while len(heap) > 0:
        cost, x, y = heapq.heappop(heap)

        if (x, y) == (h - 1, w - 1):
            return int(cost)

        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for nx, ny in neighbors:
            if 0 <= nx < w and 0 <= ny < h:
                ncost = cost + cave[nx][ny]

                if costs.get((nx, ny), np.inf) <= ncost:
                    continue

                costs[(nx, ny)] = ncost
                heapq.heappush(heap, (ncost, nx, ny))


def expand_cave(cave):
    h, w = cave.shape

    expanded = np.zeros((h * 5, w * 5))

    for i in range(5):
        for j in range(5):
            expanded[i * h : (i + 1) * h, j * w : (j + 1) * w] = cave + i + j

    while np.count_nonzero(expanded > 9) > 0:
        mask = (expanded > 9) * 1
        keep = expanded * (1 - mask)
        wrap = np.clip(np.multiply(expanded, mask) - 9, 0, 1000)
        expanded = keep + wrap

    return expanded


def preprocess_input(input_text: str):
    return np.array([list(map(int, line)) for line in input_text.split("\n")])


def first(input) -> int:
    return dijkstra(input)


def second(input) -> int:
    return dijkstra(expand_cave(input))


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=15, year=2021)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
