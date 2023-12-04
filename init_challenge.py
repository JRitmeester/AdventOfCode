#!/usr/bin/env python

import argparse
import datetime
from pathlib import Path
import os
from aoc_util.helpers import assert_session_id, load_input_data


def _init_challenges(
    days: list[int],
    year: int,
    generate_challenges: bool,
    generate_tests: bool,
    overwrite: bool,
) -> None:
    year_folder = Path.cwd() / str(year)
    year_folder.mkdir(exist_ok=True)

    if assert_session_id():
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
    today = datetime.datetime.now()

    session_id_path = Path.cwd() / '.session_id'
    if session_id_path.exists():
        SESSION_ID = session_id_path.read_text()
        # Export SESSION_ID to environment variable
        os.environ["AOC_SESSION"] = SESSION_ID

    parser.add_argument(
        "generate",
        type=str,
        choices=["all", "challenges", "tests"],
        help="What files should be generated from the template.",
        nargs="?",
        default="all",
    )

    parser.add_argument(
        "days",
        type=int,
        choices=range(0, 26),
        metavar="<0-25>",
        help="Specify date for which to generate the challenge (1-25), or 0 for all dates of a year.",
        nargs="?",
        default=today.day,
    )

    parser.add_argument(
        "year",
        type=int,
        help="Specify the year (starting at 2015) for which to generate the challenge(s).",
        nargs="?",
        default=today.year,
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