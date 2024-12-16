from collections import defaultdict, deque
import heapq
from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np


def find_all_best_paths(maze: np.ndarray, start: tuple, end: tuple) -> list:
    """Find all possible paths from start to end with their scores and full path."""
    rows, cols = maze.shape
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # E, S, W, N

    # Using deque for efficient O(1) append/pop from both ends
    # Each entry contains: (position, direction facing, current score, set of visited tiles)
    queue = deque([(start, 0, 0, {start})])

    # defaultdict avoids KeyError when checking unvisited positions
    # Stores minimum score to reach each (position, direction) combination
    visited = defaultdict(lambda: float("inf"))
    visited[(start, 0)] = 0

    # Track all paths that reach the end with the minimum score
    paths = []  # List of (score, path) tuples
    best_score = float("inf")

    while queue:
        # popleft() gives us FIFO behavior - process paths in order they were added
        pos, facing, score, path = queue.popleft()

        # If we reached the end, update best paths if this score is as good or better
        if pos == end:
            if score <= best_score:
                if score < best_score:
                    paths.clear()  # Clear worse paths when we find a better score
                    best_score = score
                paths.append((score, path))
            continue

        # Try moving in each direction
        for new_dir, (dy, dx) in enumerate(directions):
            next_y = pos[0] + dy
            next_x = pos[1] + dx
            next_pos = (next_y, next_x)

            # Skip invalid moves: out of bounds or hitting walls
            if (
                next_y < 0
                or next_y >= rows
                or next_x < 0
                or next_x >= cols
                or maze[next_y, next_x] == "#"
            ):
                continue

            # Calculate turn penalty:
            # - No cost for continuing straight
            # - 1000 for 90 degree turn
            # - 2000 for 180 degree turn
            turn_cost = 0
            if facing != new_dir:
                if abs(facing - new_dir) % 2 == 1:
                    turn_cost = 1000
                else:
                    turn_cost = 2000

            new_score = score + 1 + turn_cost

            # Only explore this path if it's at least as good as previous paths
            # to this position+direction combination
            if new_score <= visited[(next_pos, new_dir)]:
                if new_score < visited[(next_pos, new_dir)]:
                    visited[(next_pos, new_dir)] = new_score
                new_path = path.copy()
                new_path.add(next_pos)
                queue.append((next_pos, new_dir, new_score, new_path))

    return paths


def preprocess_input(input_text: str):
    return create_numpy_grid(input_text)


def first_and_second(maze: np.ndarray) -> int:
    start = get_2d_index(maze, "S")[0]
    end = get_2d_index(maze, "E")[0]
    best_paths = find_all_best_paths(maze, start, end)

    all_tiles = set()
    for _, path in best_paths:
        all_tiles.update(path)

    return best_paths[0][0], len(all_tiles)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=16, year=2024)
    preprocessed_input = preprocess_input(original_input)
    first_answer, second_answer = first_and_second(preprocessed_input)
    print("The answer to part 1 is:", first_answer)
    print("The answer to part 2 is:", second_answer)
