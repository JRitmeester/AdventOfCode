from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
import matplotlib.pyplot as plt


""" 
All numpy operations here are done using (x, y), not (y, x). This is fine as long as it's done consistently.
In reality, when debugging, the grid is transposed relative to what it should be.
"""


class Robot:

    def __init__(self, pos: np.ndarray, vel: np.ndarray):
        self.pos = np.asarray(pos)
        self.vel = np.asarray(vel)

    def move(self, grid_size: tuple[int, int]):
        self.pos += self.vel
        self.pos %= grid_size


def show_robots(robots: list[Robot], grid_size: tuple[int, int], step: int) -> None:
    grid = np.zeros(grid_size)
    for robot in robots:
        grid[tuple(robot.pos)] += 1

    if step % 101 == 19 or step % 101 == 79:
        plt.imshow(grid.T)
        plt.title(step)
        plt.show()


def preprocess_input(input_text: str):
    robot_data = [
        tuple(map(int, re.findall(r"-?\d+", line))) for line in input_text.splitlines()
    ]
    robots = [Robot((d[0], d[1]), (d[2], d[3])) for d in robot_data]
    return robots


def first(
    robots: list[Robot], grid_size: tuple[int, int] = (101, 103), steps: int = 100
) -> int:
    for _ in range(steps):
        for r in robots:
            r.move(grid_size)

    ver_center = (
        grid_size[0] // 2
    )  # Horizontal center is the vertical line in the middle of the width of the room.
    hor_center = (
        grid_size[1] // 2
    )  # Vertical center is the horizontal line in the middle of the height of the room.
    quadrants = [0, 0, 0, 0]
    for robot in robots:
        if robot.pos[0] < ver_center and robot.pos[1] < hor_center:  # Top-left
            quadrants[0] += 1
        elif robot.pos[0] > ver_center and robot.pos[1] < hor_center:  # Top-right
            quadrants[1] += 1
        elif robot.pos[0] < ver_center and robot.pos[1] > hor_center:  # Bottom-left
            quadrants[2] += 1
        elif robot.pos[0] > ver_center and robot.pos[1] > hor_center:  # Bottom-right
            quadrants[3] += 1
        else:
            pass  # Robot is exactly on the border between quadrants, ignore.
    return np.prod(quadrants)


def second(
    robots: list[Robot], grid_size: tuple[int, int] = (101, 103), steps: int = 10000
) -> None:
    """
    I visualise each frame at first, going up to 300 and noting down which iterations show some kind of pattern (more clustering)
    Then I noticed that some intervals seemed to be 101 iterations apart, and some 103, which of course is not coincidence.
    This meant that each occurrence could be expressed as a frequency (101 or 103) and an offset, which is the step number % frequency.
    So I implemented that in the show_robots function, and only had to look at 2% of all iterations, until I found the pattern.
    Then, importantly, I had to add 100 to my result, because the robots already had moved 100 steps in the first half! This could have been
    prevented by reinitialising the robots at the start of the second half, but this works too.
    """
    for i in range(steps):
        for r in robots:
            r.move(grid_size)

        show_robots(robots, grid_size, step=i + 1)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=14, year=2024)
    preprocessed_input = preprocess_input(original_input)

    print(
        "The answer to part 1 is:",
        first(preprocessed_input, grid_size=(101, 103)),
    )
    print("The answer to part 2 is:", second(preprocessed_input))
