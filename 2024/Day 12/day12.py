from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint
import itertools
import matplotlib.pyplot as plt


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def group_adjacent_coordinates(grid, char):
    """Group coordinates for a specific character using flood-fill."""
    visited = set()
    groups = []
    rows, cols = grid.shape

    def bfs(start):
        queue = [start]
        region = []
        while queue:
            y, x = queue.pop(0)
            if (y, x) in visited or grid[y, x] != char:
                continue
            visited.add((y, x))
            region.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < rows and 0 <= nx < cols and (ny, nx) not in visited:
                    queue.append((ny, nx))
        return region

    for y in range(rows):
        for x in range(cols):
            if grid[y, x] == char and (y, x) not in visited:
                groups.append(bfs((y, x)))

    return groups


def calculate_perimeter(region):
    neighbour_count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for y, x in region:
        neighbours = 0
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (y + dy, x + dx) in region:
                neighbours += 1
        neighbour_count[neighbours] += 1

    perimeter = (
        4 * neighbour_count[0]
        + 3 * neighbour_count[1]
        + 2 * neighbour_count[2]
        + 1 * neighbour_count[3]
        # + 0 * neighbour_count[4]
    )
    return perimeter


def calculate_sides(region, grid):
    """
    Calculate the number of sides for a given region by counting connected straight boundaries.
    """
    visited = set()  # Track visited edges
    sides = 0
    rows, cols = grid.shape

    def count_straight_edges(y, x, dy, dx):
        """Counts a single straight edge until it ends or changes direction."""
        ny, nx = y + dy, x + dx
        while 0 <= ny < rows and 0 <= nx < cols and (ny, nx) not in visited:
            if grid[ny, nx] != grid[y, x]:
                break  # Boundary encountered
            visited.add((ny, nx))
            ny, nx = ny + dy, nx + dx
        return 1  # Each continuous edge counts as 1 side

    for y, x in region:
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):  # Down, up, right, left
            ny, nx = y + dy, x + dx
            if not (0 <= ny < rows and 0 <= nx < cols) or grid[ny, nx] != grid[y, x]:
                # Only start counting for unvisited boundaries
                if (y, x, dy, dx) not in visited:
                    sides += count_straight_edges(y, x, dy, dx)
    return sides


def solve(grid):
    rows, cols = len(grid), len(grid[0])
    regions = []
    unvisited = set((x, y) for x in range(cols) for y in range(rows))
    while len(unvisited) > 0:
        x, y = unvisited.pop()
        type = grid[y][x]
        to_visit = [(x, y)]
        region = {(x, y)}
        fences = set()
        while len(to_visit) > 0:
            x, y = to_visit.pop()
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                nx, ny = x + dx, y + dy
                if nx < 0 or nx >= cols or ny < 0 or ny >= rows or grid[ny][nx] != type:
                    fences.add((nx, ny, dx, dy))
                    continue
                if (nx, ny) not in region:
                    region.add((nx, ny))
                    to_visit.append((nx, ny))
        unvisited -= region
        regions.append((region, fences))
    return regions


def preprocess_input(input_text: str):
    return create_numpy_grid(input_text)


def plot_regions(regions, char):
    # Plot the regions
    image = np.zeros((map.shape[0], map.shape[1]))
    for i, region in enumerate(regions):
        for y, x in region:
            image[y, x] = i

    plt.imshow(image)
    plt.title(char)
    plt.show()


def first(map: np.ndarray) -> int:
    prices = 0
    for char in np.unique(map):
        regions = group_adjacent_coordinates(map, char)
        # plot_regions(regions, char)
        for region in regions:
            area = len(region)
            perimeter = calculate_perimeter(region)
            prices += area * perimeter
    return prices


def second(map: np.ndarray) -> int:
    # total_price = 0
    # for char in np.unique(map):
    #     if char == " ":  # Skip empty spaces if any
    #         continue
    #     regions = group_adjacent_coordinates(map, char)
    #     for region in regions:
    #         area = len(region)
    #         sides = calculate_sides(region, map)
    #         total_price += area * sides
    #         print(char, area, sides, area * sides)
    # return total_price
    total = 0
    for region, fences in solve(map):
        area = len(region)
        sides = len(fences)
        for x, y, dx, dy in fences:
            if (x - 1, y, dx, dy) in fences or (x, y - 1, dx, dy) in fences:
                sides -= 1
        total += area * sides
    return total


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=12, year=2024)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
