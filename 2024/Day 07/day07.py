from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import print_timing, load_input_data
import itertools
from typing import Callable

EquationList = list[tuple[int, list[int]]]


def add(a: int, b: int) -> int:
    return a + b


def mul(a: int, b: int) -> int:
    return a * b


def concatentate(a: int, b: int) -> int:
    return int(str(a) + str(b))


def calculate_possible_answers(
    operators: list[Callable], operands: list[int], test_value: int
) -> list[int]:
    possible_answers = set()
    cache = {}  # (current_total, remaining_operands_index) -> result

    def calculate_with_cache(total: int, idx: int) -> None:
        if idx >= len(operands):
            possible_answers.add(total)
            return

        cache_key = (total, idx)
        if cache_key in cache:
            return

        for operator in operators:
            new_total = operator(total, operands[idx])
            if new_total <= test_value:  # Early stopping condition
                calculate_with_cache(new_total, idx + 1)

        cache[cache_key] = True  # Mark this combination as processed

    calculate_with_cache(operands[0], 1)
    return list(possible_answers)


def preprocess_input(input_text: str) -> EquationList:
    lines = input_text.split("\n")
    equations: EquationList = [
        (int(result), list(map(int, operands.split())))
        for result, operands in [line.split(": ") for line in lines]
    ]
    return equations


@print_timing
def first(equations: EquationList) -> int:
    return sum(
        result
        for result, operands in equations
        if result
        in calculate_possible_answers(
            operators=[add, mul], operands=operands, test_value=result
        )
    )


@print_timing
def second(equations: EquationList) -> int:
    return sum(
        result
        for result, operands in equations
        if result
        in calculate_possible_answers(
            operators=[add, mul, concatentate], operands=operands, test_value=result
        )
    )


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=7, year=2024)
    preprocessed_input = preprocess_input(original_input)

    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
