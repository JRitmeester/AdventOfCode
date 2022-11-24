from pathlib import Path
from functools import wraps
import time
from aocd import get_data

import numpy as np


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
        print(f"{func.__name__} took {(end - start) * 1000:.8f} seconds")
        return result

    return wrapper


def load_input_data(
    input_file: Path, day: int, year: int, split_by=None
) -> str | list[str]:
    if not input_file.exists():
        data = get_data(day=day, year=year)
        input_file.write_text(data)
    else:
        data = input_file.read_text()

    if split_by:
        return data.split(split_by)
    else:
        return data


def input_to_np_arr(input: str, dtype=None) -> np.ndarray:
    arr = np.array(input)
    if dtype:
        arr = arr.astype(dtype)
    return arr
