from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint
import matplotlib.pyplot as plt
from tqdm import tqdm

DIRS = {
    "^": np.array([-1, 0]),
    ">": np.array([0, 1]),
    "v": np.array([1, 0]),
    "<": np.array([0, -1]),
}


class Robot:
    def __init__(self, pos):
        self.pos = np.asarray(pos)


def show_map(
    map: np.ndarray,
    walls: np.ndarray,
    boxes: np.ndarray,
    robot: Robot,
    new: bool = False,
):
    map_render = np.zeros_like(map, dtype=int)
    for by, bx in boxes:
        map_render[by, bx] = 2
        if new:
            map_render[by, bx + 1] = 2

    for wy, wx in walls:
        map_render[wy, wx] = 1
    map_render[tuple(robot.pos)] = 3
    plt.imshow(map_render)
    plt.show(block=False)


def preprocess_input(input_text: str) -> tuple[np.ndarray, str]:
    map, instructions = input_text.split("\n\n")
    map = create_numpy_grid(map)
    instructions = instructions.replace("\n", "")
    return map, instructions


def first(map: np.ndarray, instructions: str) -> int:
    walls = np.argwhere(map == "#")
    boxes = np.argwhere(map == "O")
    robot = np.argwhere(map == "@")
    plt.figure(figsize=(5, 5))

    robot = Robot(robot[0])
    for dir in tqdm(instructions):
        # show_map(map, walls, boxes, robot)
        # If the robot moves into a box, move the box in the same direction. If the box moves into another box, move that box in the same direction, and so on,
        # Until the box can't move anymore because it's against a wall.
        boxes_to_move = []

        if any(np.array_equal(robot.pos + DIRS[dir], wall) for wall in walls):
            continue
        else:
            # Check if there is a row of boxes between the robot and a wall, preventing the robot from moving into the boxes
            i = 0
            while True:
                pos_to_check = robot.pos + DIRS[dir] * (i + 1)
                if any(np.array_equal(pos_to_check, box) for box in boxes):
                    box_id = np.argwhere(
                        [tuple(box) == tuple(pos_to_check) for box in boxes]
                    ).item()
                    boxes_to_move.append(box_id)
                    i += 1
                    continue
                if not any(np.array_equal(pos_to_check, wall) for wall in walls):
                    robot.pos += DIRS[dir]
                    for box_id in boxes_to_move:
                        boxes[box_id] += DIRS[dir]
                break
    total = 0
    for box in boxes:
        total += box[0] * 100 + box[1]
    return total


def rework_map(map: np.ndarray) -> np.ndarray:
    new_map = np.zeros((map.shape[0] * 1, map.shape[1] * 2), dtype="<U1")
    # Where "#" was on the old map, insert two adjacent "#"s on the new map
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == "#":
                new_map[y, x * 2] = "#"
                new_map[y, x * 2 + 1] = "#"
            elif cell == "O":
                new_map[y, x * 2] = "["
                new_map[y, x * 2 + 1] = "]"
            elif cell == "@":
                new_map[y, x * 2] = "@"
                new_map[y, x * 2 + 1] = "."

    return new_map


# 2885149 too high
def second(map, instructions) -> int:
    # Create the new, doubled-width map
    new_map = rework_map(map)
    # plt.figure(figsize=(5, 5))

    # Initialize positions
    walls = np.argwhere(new_map == "#")
    boxes = np.argwhere(new_map == "[")
    robot = np.argwhere(new_map == "@")[0]
    robot = Robot(robot)

    for j, dir in tqdm(enumerate(instructions), total=len(instructions)):
        # If the robot hits a wall, skip the move
        if j == 19999:
            show_map(new_map, walls, boxes, robot, new=True)
        if any(np.array_equal(robot.pos + DIRS[dir], wall) for wall in walls):
            continue

        # Check for boxes in the direction of movement
        boxes_to_move = set()
        boxes_to_check = {
            tuple(robot.pos + DIRS[dir])
        }  # Start with position in front of robot
        checked_positions = set()

        starting_pos = robot.pos.copy()
        while boxes_to_check:
            pos = np.array(boxes_to_check.pop())
            if tuple(pos) in checked_positions:
                continue
            checked_positions.add(tuple(pos))

            # Check if this position hits any box
            for box_idx, box in enumerate(boxes):
                if np.array_equal(pos, box) or np.array_equal(pos, box + [0, 1]):
                    boxes_to_move.add(box_idx)
                    # Add positions to check: in front of box and in front of right side of box
                    boxes_to_check.add(tuple(boxes[box_idx] + DIRS[dir]))
                    boxes_to_check.add(tuple(boxes[box_idx] + DIRS[">"] + DIRS[dir]))

        # Check if all boxes can move
        can_move = True
        for box_id in boxes_to_move:
            new_box_pos = boxes[box_id] + DIRS[dir]
            new_box_pos_right = new_box_pos + [0, 1]
            if any(np.array_equal(new_box_pos, wall) for wall in walls) or any(
                np.array_equal(new_box_pos_right, wall) for wall in walls
            ):
                can_move = False
                break

        if can_move:
            robot.pos += DIRS[dir]
            for box_id in boxes_to_move:
                boxes[box_id] += DIRS[dir]

    # Calculate GPS coordinates for the wide boxes
    total = 0
    for box in boxes:
        total += box[0] * 100 + box[1]
    plt.show()
    return total


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=15, year=2024)
    preprocessed_input = preprocess_input(original_input)
    # print("The answer to part 1 is:", first(*preprocessed_input))
    print("The answer to part 2 is:", second(*preprocessed_input))
