from pathlib import Path
from typing import List, Union

import shutil
import argparse
from functools import wraps
import time


def print_timing(func: callable) -> callable:
    """
    create a timing decorator function
    use `@print_timing `just above the function you want to time
    """

    @wraps(func)  # improves debugging
    def wrapper(*arg):
        start = time.perf_counter()  # needs python3.3 or higher
        result = func(*arg)
        end = time.perf_counter()
        print(f"{func.__name__} took {(end - start) * 1000:.8f} seconds")
        return result

    return wrapper


def load_input_data(day: int, year: int, split_by=None) -> Union[str, List[str]]:
    data_path = Path.cwd() / str(year) / f"Day {str(day).zfill(2)}" / "input.txt"
    data = data_path.read_text()

    if split_by:
        return data.split(split_by)
    else:
        return data



