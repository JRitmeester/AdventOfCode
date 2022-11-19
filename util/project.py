#!/usr/bin/env python
from pathlib import Path
from typing import List, Union
from aocd import get_data
import shutil
import argparse
from functools import wraps
import time


def _init_year(year) -> None:
    template = (Path.cwd() / "template.txt").read_text()

    year_folder = Path.cwd().parent / str(year)
    year_folder.mkdir(exist_ok=True)

    if _assert_session_id():
        for day_number in range(1, 26):
            day_number_fmt = str(day_number).zfill(2)

            day_folder = year_folder / f"Day {day_number_fmt}"
            day_folder.mkdir(exist_ok=True)

            python_file = day_folder / f"day{day_number_fmt}.py"
            if not python_file.exists():
                python_file.write_text(template.format(day_number, year))

            input_file = day_folder / "input.txt"
            if not input_file.exists():
                input_data = get_data(day=day_number, year=year)
                input_file.write_text(input_data)


def _assert_session_id() -> None:
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--init-year",
        type=int,
        help="Initialise a folder with the appropriate data for the given year",
    )
    args = vars(parser.parse_args())

    if args["init_year"]:
        _init_year(args["init_year"])
