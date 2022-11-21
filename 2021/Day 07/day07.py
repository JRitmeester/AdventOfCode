from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math


def get_nth_triangle_number(n):
    """
    Triangle numbers are for summing what factorials are for multiplication.
    """
    return (n * n + n) / 2


def main():
    input_raw = (Path(__file__).parent / "input.txt").read_text()
    positions = np.array([int(x) for x in input_raw.split(",")])

    # Part 1: Calculate the total distance travelled by all the crabs, and find the
    # minimal fuel usage.
    fuel_usages = np.sum([np.abs(positions - x) for x in range(max(positions))], axis=1)
    best_position, minimal_fuel_usage = np.argmin(fuel_usages), np.min(fuel_usages)
    print(f"The minimal fuel usage (part 1) is {minimal_fuel_usage}")

    # Part 2:
    fuel_usages = np.sum(
        [get_nth_triangle_number(np.abs(positions - x)) for x in range(max(positions))],
        axis=1,
    )
    best_position, minimal_fuel_usage = np.argmin(fuel_usages), np.min(fuel_usages)
    print(f"The minimal fuel usage (part 2) is {minimal_fuel_usage}")


if __name__ == "__main__":
    main()
