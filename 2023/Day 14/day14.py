from pathlib import Path

from tqdm import tqdm; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
import numpy as np; np.set_printoptions(threshold=sys.maxsize)

from aoc_util.helpers import *
from pprint import pprint

def preprocess_input(input_text: str) -> np.ndarray:
    return create_numpy_grid(input_text)


def move_platform(platform: np.ndarray, direction: str) -> np.ndarray:
    """Move the boulders in the given direction. The direction is changed to be "up" by rotating the platform, so that the movement itself can be done column-wise
    regardless of the actual direction."""

    n_rotations = list(DIRS).index(direction)  # The number of rotations needed to orient the platform in the correct way
    platform = np.rot90(platform, k=n_rotations) # Rotate the platform so that the movement can be done column-wise

    # Loop along each element in the platform.
    for col in range(platform.shape[1]):
        for row in range(platform.shape[0]):

            current = platform[row, col]
            if current != 'O':  # Skip if the current position is not a round boulder.
                continue

            # Move the boulder as far as possible in the given direction.
            new_row = row
            while True:

                # Check the position above the current boulder.
                new_row -= 1
                if new_row < 0:  # Out of bounds
                    break
                
                # If the boulder is obstructed by another round boulder, or a square one, stop moving.
                next_position = platform[new_row, col]
                if next_position in ['O', '#']:
                    break
            
            # Set the new position of the boulder, and clear the old one.
            platform[row, col] = '.'
            platform[new_row+1, col] = 'O'

    # Undo the rotation of the platform done at the start.                     
    platform = np.rot90(platform, k=-n_rotations)
    return platform


def calculate_load(platform: np.ndarray) -> int:
    """Calculate the load of the platform, i.e. the sum of the scores of all the boulders.
    The score of each boulder is its distance away from the southern edge."""

    n_rows = platform.shape[0]
    total = np.sum([(n_rows - row) * np.sum(platform[row] == 'O') for row in range(n_rows)])
    return total


def do_cycle(platform: np.ndarray) -> np.ndarray:
    """Perform a single cycle of the platform, i.e. move the boulders in all directions once."""
    for direction in ["up", "left", "down", "right"]:
        platform = move_platform(platform, direction)
    return platform


def perform_spin_cycles(platform: np.ndarray) -> np.ndarray:
    """Perform a billion spin cycles on the platform, and return the platform after the last cycle.
    The first cycles are cached in order to detect loops in the platform, and skip ahead to the last cycle."""
    
    N_CYCLES = 1_000_000_000

    history = []
    cycle = 0
    found = False

    while cycle < N_CYCLES:
        cycle += 1
        platform = do_cycle(platform)

        # Create a representation of the platform to use as a key in the cache.
        key = platform.tolist()

        # Once a platform configuration has been found
        if key in history and not found:
            found = True
            cycle_start_index = history.index(key)  # Look up when it was first found

            # Calculate the loop length as the difference between the current cycle and the first cycle it was found
            loop_length = cycle - cycle_start_index -1  

            # Calculate the number of cycles left to perform
            cycles_left = (N_CYCLES - cycle) % loop_length

             # Skip ahead to the last cycle
            cycle = N_CYCLES - cycles_left 
        
        else:
            # Store the platform configuration in the cache
            history.append(key)

    return platform


def first(platform: np.ndarray) -> int:
    platform = move_platform(platform, "up")
    score  = calculate_load(platform)
    return score


def second(platform: np.ndarray) -> int:
    platform = perform_spin_cycles(platform)
    score = calculate_load(platform)
    return score


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=14, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
