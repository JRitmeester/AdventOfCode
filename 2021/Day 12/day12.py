"""
All credits to Github user Rtchaik (https://github.com/Rtchaik/AoC-2021) for this solution.
I have changed it to learn from it by decomposing and restructuring the functions.
"""

from collections import defaultdict
from pathlib import Path


def find_number_of_routes(connections, path):

    total = 0

    # Check the cave that was added last, and explore its connections.
    for cave in connections[path[-1]]:

        # If it is a big cave, or it hasn't been explored yet,
        # check if the cave is the end. If not, explore its connectinos
        # by calling this functions again with this cave added to the path.
        if cave.isupper() or cave not in path:

            # If it's the end, just add one to the total number of routes.
            # Otherwise, keep searching.
            if cave == "end":
                total += 1
            else:
                total += find_number_of_routes(connections, path + [cave])
    return total


def find_number_of_routes2(connections, path):
    total = 0
    for cave in connections[path[-1]]:
        if cave == "end":
            total += 1
        else:
            if cave.islower() and cave in path:
                num_routes = find_number_of_routes(connections, path + [cave])
            else:
                num_routes = find_number_of_routes2(connections, path + [cave])
            total += num_routes
    return total


def main():
    input_raw = (Path(__file__).parent / "input.txt").read_text()
    connections = defaultdict(list)

    for line in input_raw.split("\n"):
        pair = line.split("-")

        # Add a two-way connection between cave a and b,
        # for each connection in the input file.
        for a, b in zip(pair, reversed(pair)):
            if b != "start":
                connections[a].append(b)

    print("Answer part 1: ", find_number_of_routes(connections, ["start"]))
    print("Answer part 2: ", find_number_of_routes2(connections, ["start"]))


if __name__ == "__main__":
    main()
