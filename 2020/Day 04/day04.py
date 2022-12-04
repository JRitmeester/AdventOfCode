import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())

from aoc_util.helpers import load_input_data, print_timing


@print_timing
def preprocess_input(input_text: str):
    passports_str = input_text.split("\n\n")

    passports = []
    for passport_str in passports_str:
        passport_str = " ".join(passport_str.split("\n"))
        passport = {}
        pairs = passport_str.split(" ")
        for pair in pairs:
            key, val = pair.split(":")
            passport[key] = val
        passports.append(passport)
    return passports


@print_timing
def first(passports) -> int:
    valid = 0
    expected_fields = sorted(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    for passport in passports:
        if all(expected_key in passport.keys() for expected_key in expected_fields):
            valid += 1
    return valid


@print_timing
def second(passports) -> int:
    valid = 0
    hexa_str = 'abcdef1234567890'
    expected_fields = sorted(["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"])
    for passport in passports:
        if all(expected_key in passport.keys() for expected_key in expected_fields):
            print(passport)
            byr_valid = 1920 <= int(passport["byr"]) <= 2002
            print("byr", byr_valid)
            iyr_valid = 2010 <= int(passport["iyr"]) <= 2020
            print("iyr", iyr_valid)
            eyr_valid = 2020 <= int(passport["eyr"]) <= 2030
            print("eyr", eyr_valid)
            hgt_valid = (
                passport["hgt"][-2:] == "cm" and 150 <= int(passport["hgt"][:-2]) <= 193
            ) or (
                passport["hgt"][-2:] == "in" and 59 <= int(passport["hgt"][:-2]) <= 76
            )
            print("hgt", hgt_valid)
            hcl_valid = (passport["hcl"][0] == "#") and all([char.lower() in hexa_str for char in passport['hcl'][1:]])
            print("hcl", hcl_valid)
            ecl_valid = passport["ecl"] in [
                "amb",
                "blu",
                "brn",
                "gry",
                "grn",
                "hzl",
                "oth",
            ]
            print("ecl", ecl_valid)
            pid_valid = len(passport["pid"]) == 9
            print("pid", pid_valid)
            if (
                byr_valid
                and iyr_valid
                and eyr_valid
                and hgt_valid
                and hcl_valid
                and ecl_valid
                and pid_valid
            ):
                valid += 1

    return valid


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=4, year=2020)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
