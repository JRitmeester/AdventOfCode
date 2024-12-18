import heapq
import shutil
import time
from functools import wraps
from pathlib import Path

import numpy as np
from aocd import get_data

DIRS = {
    "right": np.array([0, 1]),
    "down": np.array([1, 0]),
    "left": np.array([0, -1]),
    "up": np.array([-1, 0]),
}


def assert_session_id() -> bool:
    """
    Ensures the Session ID is set in $HOME/.config/aocd/token, from which aocd retrieves it automatically. If it is
    not set already, this function will try to retrieve it from the .session_id file from the root of the project
    directory.
    """
    session_id_file = Path("~").expanduser() / ".config/aocd/token"
    if not session_id_file.exists():
        session_id_local = Path.cwd() / ".session_id"
        if session_id_local.exists():
            session_id_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(session_id_local, session_id_file)
        else:
            print(
                f"No session ID could be found in {session_id_file.as_posix()} or {session_id_local.as_posix()}."
            )
    return session_id_file.exists()


def print_timing(func: callable) -> callable:
    """
    create a timing decorator function
    use `@print_timing `just above the function you want to time
    """

    @wraps(func)
    def wrapper(*arg):
        start = time.perf_counter()
        result = func(*arg)
        end = time.perf_counter()
        print(f"{func.__name__} took {(end - start):.8f} seconds")
        return result

    return wrapper


def load_input_data(
    input_file: Path, day: int, year: int, store_data: bool = True
) -> str | list[str]:
    if not input_file.exists():
        data = get_data(day=day, year=year)
        if store_data:
            input_file.write_text(data)
    else:
        data = input_file.read_text()

    return data


def create_numpy_grid(multiline_string: str) -> np.ndarray:
    grid = np.array([list(line) for line in multiline_string.split("\n")])
    return grid


def get_2d_index(arr: np.ndarray, element: any) -> list[tuple[int, int]]:
    """Returns a list (y,x) pairs where `element` is found in `grid`.

    Args:
        grid (np.ndarray): Input array
        element (any): Element to search for

    Returns:
        list[tuple[int, int]]: List of 2D indices as [(y,x), ...]
    """
    return list(zip(*np.where(arr == element)))


def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def a_star(grid: np.ndarray, start: tuple, end: tuple) -> tuple[int, list]:
    """A* pathfinding algorithm to find shortest path between start and end positions.

    Args:
        grid: numpy array where 0 is path and 1 is wall
        start: (y,x) starting coordinates
        end: (y,x) ending coordinates

    Returns:
        Tuple of (best path score, list of coordinates for best path)
    """
    rows, cols = grid.shape
    directions = DIRS.values()  # right, down, left, up

    # Priority queue storing: (f_score, position, path_so_far)
    # f_score = g_score (distance from start) + h_score (estimated distance to end)
    open_set = [(manhattan_distance(start, end), start, [start])]

    # Track g_scores (actual distance from start to each position)
    g_scores = {start: 0}

    while open_set:
        _, current_pos, current_path = heapq.heappop(open_set)

        if current_pos == end:
            return g_scores[current_pos], current_path

        for dy, dx in directions:
            next_y, next_x = current_pos[0] + dy, current_pos[1] + dx
            next_pos = (next_y, next_x)

            # Check bounds and walls
            if (
                next_y < 0
                or next_y >= rows
                or next_x < 0
                or next_x >= cols
                or grid[next_y, next_x] == 1
            ):
                continue

            # Calculate new g_score for this neighbor
            tentative_g_score = g_scores[current_pos] + 1

            # Only proceed if this path to neighbor is better than any previous one
            if next_pos not in g_scores or tentative_g_score < g_scores[next_pos]:
                g_scores[next_pos] = tentative_g_score
                f_score = tentative_g_score + manhattan_distance(next_pos, end)
                new_path = current_path + [next_pos]
                heapq.heappush(open_set, (f_score, next_pos, new_path))

    return float("inf"), []  # No path found
