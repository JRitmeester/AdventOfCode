from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import re
import json


def preprocess_input(input_text: str):
    return input_text


def first(input_data) -> int:
    return sum([int(n) for n in re.findall("-?\d+", input_data)])


def second(input_data) -> int:
    json_ = json.loads(input_data)

    def remove_red(json_obj):
        json_type = type(json_obj)
        if json_type == list:
            json_obj = [remove_red(item) for item in json_obj if item != "red"]

        elif json_type == dict:
            if any(val == "red" for val in json_obj.values()):
                json_obj = {}
            else:
                for key, val in json_obj.items():
                    json_obj[key] = remove_red(val)
        else:
            return json_obj
        return json_obj

    return sum([int(n) for n in re.findall("-?\d+", str(remove_red(json_)))])


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=12, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
