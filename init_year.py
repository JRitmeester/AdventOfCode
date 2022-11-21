#!/usr/bin/env python

from aocd import get_data
from pathlib import Path
import shutil
import argparse
import datetime
from util.project import load_input_data


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


def _init_year(year) -> None:
    template = (Path.cwd() / "template.txt").read_text()

    year_folder = Path.cwd() / str(year)
    year_folder.mkdir(exist_ok=True)

    if _assert_session_id():
        for day_number in range(1, 26):
            day_number_fmt = str(day_number).zfill(2)

            day_folder = year_folder / f"Day {day_number_fmt}"
            day_folder.mkdir(exist_ok=True)

            python_file = day_folder / f"day{day_number_fmt}.py"
            if not python_file.exists():
                python_file.write_text(template.format(day_number, year))

            load_input_data(
                input_file=day_folder / "input.txt", day=day_number, year=year
            )
            # input_file = day_folder / "input.txt"
            # if not input_file.exists():
            #     input_data = get_data(day=day_number, year=year)
            #     input_file.write_text(input_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "init-year",
        type=int,
        help="Initialise a folder with the appropriate data for the given year",
    )
    args = vars(parser.parse_args())
    year = args["init-year"]
    if year:
        if 2015 <= year <= datetime.datetime.now().year:
            _init_year(year)
        else:
            parser.error(f"There is no Advent of Code for the year {year}.")
    else:
        parser.error("Please specify a year between 2015 and the current year.")
