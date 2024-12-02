from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint


def preprocess_input(input_text: str):
    reports = input_text.split("\n")
    reports_num = []
    for report in reports:
        reports_num.append([int(x) for x in report.split(" ")])
    return reports_num


def check_report(report: list[int]) -> bool:
    differentiated_report = np.diff(report)
    if not (all(differentiated_report > 0) or all(differentiated_report < 0)):
        return False
    if 1 <= np.max(np.abs(differentiated_report)) <= 3:
        return True
    else:
        return False


def first(input_data) -> int:
    safe_count = 0
    for report in input_data:
        safe_count += check_report(report)

    return safe_count


def second(input_data: list[list[int]]) -> int:
    safe_count = 0
    for report in input_data:
        is_safe = check_report(report)
        if is_safe:
            safe_count += 1
            continue

        for i in range(len(report)):
            problem_dampener_report = report.copy()
            problem_dampener_report.pop(i)
            is_safe = check_report(problem_dampener_report)
            if is_safe:
                safe_count += 1
                break

    return safe_count


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=2, year=2024)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
