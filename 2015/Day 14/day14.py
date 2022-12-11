from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt


class Reindeer:
    def __init__(self, name: str, speed: int, duration: int, rest_time: int):
        self.name = name
        self.speed = speed
        self.duration = duration
        self.rest_time = rest_time
        self.distance = 0

    def move(self, time):
        time = time % (self.duration + self.rest_time)
        if time < self.duration:
            self.distance += self.speed

    def __repr__(self):
        return f"<Reindeer {self.name}, distance={self.distance}, speed={self.speed}, duration={self.duration}>"


def preprocess_input(input_text: str):
    reindeer = []
    for line in input_text.split("\n"):
        name = line.split(" ")[0]
        speed, duration, rest_time = [int(n) for n in re.findall(r"\d+", line)]
        reindeer.append(Reindeer(name, speed, duration, rest_time))
    return reindeer


def first(reindeer, max_time=2503) -> int:
    for time in range(max_time):
        for r in reindeer:
            r.move(time)
    return max([r.distance for r in reindeer])


def second(reindeer, max_time=2503) -> int:
    for r in reindeer:
        r.distance = 0
    score = {r.name: 0 for r in reindeer}
    for time in range(max_time):
        for r in reindeer:
            r.move(time)
        lead = [r.name for r in reindeer if r.distance == max([r_.distance for r_ in reindeer])]  # fmt:skip
        for name in lead:
            score[name] += 1
    return max(score.values())


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=14, year=2015)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
