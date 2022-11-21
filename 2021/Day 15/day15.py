import heapq
from pathlib import Path
from pprint import pprint
import numpy as np


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
            return cost

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


def main():
    input_raw = (Path(__file__).parent / "input.txt").read_text()
    cave = np.array([list(map(int, line)) for line in input_raw.split("\n")])

    print("Answer part 1:", dijkstra(cave))
    print("Answer part 2:", dijkstra(expand_cave(cave)))


if __name__ == "__main__":
    main()
