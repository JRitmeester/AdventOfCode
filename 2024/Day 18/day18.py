from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import a_star, load_input_data
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


def show_grid(grid: np.ndarray, path: list[tuple]) -> None:
    plt.figure()
    render = grid.copy()
    for y, x in path:
        render[y, x] = 2

    plt.imshow(render)
    plt.show()


def fill_memory_space(
    data: list[tuple], grid_size: tuple[int, int], n_bytes: int
) -> np.ndarray:
    grid = np.zeros(grid_size)
    for i, coordinates in enumerate(data):
        if i >= n_bytes:
            break
        grid[coordinates[1], coordinates[0]] = 1
    return grid


def preprocess_input(input_text: str) -> list[tuple[int, int]]:
    coordinates = [tuple(map(int, x.split(","))) for x in input_text.split("\n")]
    return coordinates


def first(
    coordinates: list[tuple[int, int]], grid_size: int = (7, 7), n_bytes=12
) -> int:
    start = (0, 0)
    end = (grid_size[0] - 1, grid_size[1] - 1)

    grid = fill_memory_space(coordinates, grid_size, n_bytes)
    best_path = a_star(grid, start, end)
    show_grid(grid, best_path[1])
    return best_path[0]


def second(coordinates: list[tuple[int, int]], grid_size: int = (7, 7)) -> int:
    start = (0, 0)
    end = (grid_size[0] - 1, grid_size[1] - 1)

    for n_bytes in range(1, len(coordinates)):
        grid = fill_memory_space(coordinates, grid_size, n_bytes)
        best_path = a_star(grid, start, end)
        if len(best_path[1]) == 0:
            return ",".join(map(str, coordinates[n_bytes - 1]))


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=18, year=2024)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input, (71, 71), 1024))
    print("The answer to part 2 is:", second(preprocessed_input, (71, 71)))
