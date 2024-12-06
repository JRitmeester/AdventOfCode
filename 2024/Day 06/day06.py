from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data, create_numpy_grid, DIRS, print_timing
import numpy as np
import re
from pprint import pprint
import multiprocessing
import matplotlib.pyplot as plt

USE_MULTIPROCESSING = True
DO_VISUALISATION = False


class Guard:

    def __init__(self, start_position: np.ndarray):
        self.pos = start_position
        self.dir = "up"
        self.done = False

    def move(self, lab: np.ndarray) -> None:
        # First check if next position would be out of bounds
        next_position = self.pos + DIRS[self.dir]
        if (
            next_position[0] < 0
            or next_position[0] >= lab.shape[0]
            or next_position[1] < 0
            or next_position[1] >= lab.shape[1]
        ):
            self.done = True
            return

        # Check if there's an obstacle ahead
        grid_value = lab[tuple(next_position)]
        if grid_value == "#":
            self.turn()  # Turn right if obstacle ahead
        else:
            # Move forward if no obstacle
            self.pos = next_position

    def turn(self):
        match self.dir:
            case "up":
                self.dir = "right"
            case "right":
                self.dir = "down"
            case "down":
                self.dir = "left"
            case "left":
                self.dir = "up"


def preprocess_input(input_text: str):
    lab = create_numpy_grid(input_text)
    return lab


def do_basic_route(lab: np.ndarray) -> np.ndarray:
    start_y, start_x = np.where(lab == "^")
    start_position = np.array([start_y[0], start_x[0]])
    guard = Guard(start_position)
    visited_mask = np.zeros_like(lab, dtype=bool)
    visited_mask[tuple(start_position)] = True

    while not guard.done:
        guard.move(lab)
        visited_mask[tuple(guard.pos)] = True

    return visited_mask


def first(visited_mask: np.ndarray) -> int:
    return np.sum(visited_mask)


def detect_loop(args: tuple[np.ndarray, tuple[int, int]]) -> tuple[int, int] | None:
    """Traverse the lab starting at ^ and see if the guard gets stuck in a loop."""
    lab, obstacle_position = args
    lab_copy = lab.view()
    start_position = np.where(lab_copy == "^")
    start_position = np.array([start_position[0][0], start_position[1][0]])

    lab_copy[tuple(obstacle_position)] = "#"  # Insert the obstacle
    guard = Guard(start_position)
    visited_states = set()

    while not guard.done:
        guard.move(lab_copy)

        if guard.done:
            break

        # Check if the guard has been in this state before
        state = (*tuple(guard.pos), guard.dir)
        if state in visited_states:

            return obstacle_position

        visited_states.add(state)

    if not USE_MULTIPROCESSING and DO_VISUALISATION:
        visited_states_image = np.zeros_like(lab_copy, dtype=int)
        for visited_state in visited_states:
            visited_states_image[tuple(visited_state[:2])] = -1
            # Draw the obstacles
        all_obstacles = zip(*np.where(lab_copy == "#"))
        for obstacle in all_obstacles:
            y, x = obstacle
            visited_states_image[y, x] = 2
        plt.imshow(visited_states_image, vmin=-1, vmax=2)
        plt.show()
    return None


@print_timing
def second(lab: np.ndarray, visited_mask: np.ndarray) -> int:
    # Try to place obstacles in all visited positions of the original lab. Any other obstacle would be ignored anyway.
    visited_positions = np.array(np.where(visited_mask == True)).T

    # Filter out the start position and existing obstacles
    obstacle_positions = [
        pos
        for pos in visited_positions
        if (lab[tuple(pos)] != "^" and lab[tuple(pos)] != "#")
    ]

    if USE_MULTIPROCESSING:
        num_processes = multiprocessing.cpu_count() - 1
        with multiprocessing.Pool(num_processes) as pool:
            results = pool.map(detect_loop, [(lab, pos) for pos in obstacle_positions])
    else:
        results = [detect_loop((lab, pos)) for pos in obstacle_positions]

    results = [result for result in results if result is not None]
    return len(results)  # Count how obstacles configurations result in loops


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=6, year=2024)
    preprocessed_input = preprocess_input(original_input)
    visited_mask = do_basic_route(preprocessed_input)
    print("The answer to part 1 is:", first(visited_mask))
    print("The answer to part 2 is:", second(preprocessed_input, visited_mask))
