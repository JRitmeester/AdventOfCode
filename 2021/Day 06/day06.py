import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint


def create_map(lines: list, include_diagonal: bool):
    grid = np.zeros((2000, 2000))

    max_x = 0
    max_y = 0

    for line in lines:
        start = np.array(line[0])
        end = np.array(line[1])
        delta = np.array([end[0] - start[0], end[1] - start[1]])
        length = np.max(np.abs(delta))
        dir = delta / length

        if not include_diagonal:
            if np.sum(np.abs(dir)) != 1:
                continue

        for step in range(length + 1):
            current = (start + step * dir).astype(np.int)
            grid[current[1], current[0]] += 1
            max_x = max(max_x, current[0])
            max_y = max(max_y, current[1])

    grid = grid[:max_y, :max_x]

    return grid


def main():
    input_raw = (Path(__file__).parent / "input.txt").read_text()
    input_split = input_raw.split("\n")[:-1]
    lines = [
        [tuple(int(el) for el in point.split(",")) for point in line.split(" -> ")]
        for line in input_split
    ]

    # Part 1
    grid = create_map(lines, include_diagonal=False)
    plt.imshow(grid)
    print("Answer part 1:", np.count_nonzero(grid > 1))

    # Part 2
    grid = create_map(lines, include_diagonal=True)
    plt.imshow(grid)
    print("Answer part 2:", np.count_nonzero(grid > 1))

    plt.show()


if __name__ == "__main__":
    main()
