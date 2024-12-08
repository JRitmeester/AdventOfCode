import shutil
import time
from functools import wraps
from pathlib import Path

import numpy as np
from aocd import get_data

DIRS = {
    "up": np.array([-1, 0]),
    "right": np.array([0, 1]),
    "down": np.array([1, 0]),
    "left": np.array([0, -1]),
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
