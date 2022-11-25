#!/usr/bin/env python

import argparse
import datetime
import shutil
from pathlib import Path

from aocd import get_data

from aoc_util.helpers import load_input_data


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


def _init_challenges(
    days: list[int],
    year: int,
    generate_challenges: bool,
    generate_tests: bool,
    overwrite: bool,
) -> None:
    year_folder = Path.cwd() / str(year)
    year_folder.mkdir(exist_ok=True)

    if _assert_session_id():
        for day_number in days:
            challenge_template = (Path.cwd() / "challenge_template.txt").read_text()
            test_template = (Path.cwd() / "test_template.txt").read_text()

            day_number_fmt = str(day_number).zfill(2)
            day_folder = year_folder / f"Day {day_number_fmt}"
            day_folder.mkdir(exist_ok=True)

            if generate_challenges:
                python_file = day_folder / f"day{day_number_fmt}.py"
                if not python_file.exists() or overwrite:
                    python_file.write_text(challenge_template.format(day_number, year))

                    load_input_data(
                        input_file=day_folder / "input.txt",
                        day=day_number,
                        year=year,
                        store_data=True,
                    )

            if generate_tests:
                example_input_file = day_folder / f"example_input.txt"
                if not example_input_file.exists() or overwrite:
                    example_input_file.write_text("")

                test_file = day_folder / f"day{day_number_fmt}_test.py"
                if not test_file.exists() or overwrite:
                    test_file.write_text(
                        test_template.format(day_number_fmt.lower(), day_number, year)
                    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "generate",
        type=str,
        choices=["all", "challenges", "tests"],
        help="What files should be generated from the template.",
    )

    parser.add_argument(
        "days",
        type=int,
        choices=range(0, 26),
        metavar="<0-25>",
        help="Specify date for which to generate the challenge (1-25), or 0 for all dates of a year.",
    )

    parser.add_argument(
        "year",
        type=int,
        help="Specify the year (starting at 2015) for which to generate the challenge(s).",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the existing files for all specified challenges.",
    )

    args = vars(parser.parse_args())
    generate, days, year = args["generate"], args["days"], args["year"]

    generate_challenges = generate in ["challenges", "all"]
    generate_tests = generate in ["tests", "all"]
    overwrite = args["overwrite"]

    if 2015 <= year <= datetime.datetime.now().year:
        if 0 <= days <= 25:
            _init_challenges(
                days=(range(1, 26) if days == 0 else [days]),
                year=year,
                generate_challenges=generate_challenges,
                generate_tests=generate_tests,
                overwrite=overwrite,
            )
        else:
            parser.error(
                f"Advent of Code starts at December 1st and ends on December 25th."
            )
    else:
        parser.error("Please specify a year between 2015 and the current year.")
