from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *


def expand_disk(dense_format: str, nested=False) -> list[str]:
    """
    Go through the dense format and expand it into a disk string by
    alternating between file blocks and empty blocks.
    Append the id of the file block to the disk string, followed by the
    number of empty blocks.

    Example:
    12345 --> 0..111....22222
    Args:
        dense_format (str): The dense format to expand.

    Returns:
        str: The expanded disk string.
    """
    is_file_block = True
    expanded_disk = []
    id = 0

    for x in dense_format:
        if is_file_block:
            addition = [str(id)] * int(x)
            id += 1  # Increment the id for the next file block
        else:
            addition = ["."] * int(x)
        if int(x) > 0:
            if nested:
                expanded_disk.append(addition)
            else:
                expanded_disk.extend(addition)

        is_file_block = not is_file_block  # Toggle the block type
    return expanded_disk


def sort_disk_one_by_one(disk: list[str]) -> list[str]:
    """
    Sort the disk by moving the empty blocks to the end of the disk and
    inserting the file blocks one-by-one in the empty blocks, in reverse order.

    Note that in the final result, all the empty blocks are at the end of the
    disk. Therefore, you can count the number of empty blocks and find the division
    between the static data at the start of the disk, and the data that needs to
    be inserted in reverse in the empty blocks.

    Example:
    0..111....22222
    02.111....2222.
    022111....222..
    0221112...22...
    02211122..2....
    022111222......
    022111222

    Args:
        disk (str): The disk to sort.

    Returns:
        str: The sorted disk.
    """
    sorted_disk = []

    j = len(disk) - 1
    for i in range(len(disk) - disk.count(".")):
        if disk[i] != ".":
            sorted_disk.append(disk[i])
        else:
            while True:
                insert_char = disk[j]
                if insert_char != ".":
                    sorted_disk.append(insert_char)
                    j -= 1
                    break
                j -= 1

    return sorted_disk


def sort_disk_file_by_file(disk: list[str]) -> list[str]:
    """
    Sort the disk by moving the empty blocks to the end of the disk and
    inserting the file blocks in the empty blocks, in reverse order.

    00...111...2...333.44.5555.6666.777.888899
    0099.111...2...333.44.5555.6666.777.8888..
    0099.1117772...333.44.5555.6666.....8888..
    0099.111777244.333....5555.6666.....8888..
    00992111777.44.333....5555.6666.....8888..
    """

    # See if each file can be moved, but only once. So we can iterate over each file once.
    moveable_files = [x for x in reversed(disk.copy()) if "." not in x]
    for moveable_file in moveable_files:
        # Search for empty blocks large enough to fit the file.
        for block_index, block in enumerate(disk):

            # If the block is the file itself, stop looking, to prevent moving them farther right.
            if block == moveable_file:
                break

            # Afterwards, check if it is a free space or not.
            if "." not in block:
                continue

            file_size = len(block)
            moveable_file_size = len(moveable_file)

            # Check if the file can fit in the block.
            if moveable_file_size <= file_size:
                difference = file_size - moveable_file_size

                # First, remove the old empty block.
                disk.remove(block)

                # Then, insert the new empty block, if there is a difference.
                if difference > 0:
                    disk.insert(block_index, ["."] * difference)

                # Then, insert the file at the right position.
                disk[disk.index(moveable_file)] = ["."] * moveable_file_size
                disk.insert(block_index, moveable_file)

                # Merge empty blocks, i.e. ["."],["."] --> [".","."]
                i = 0
                while i < len(disk) - 1:
                    if "." in disk[i] and "." in disk[i + 1]:
                        new_block = ["."] * (len(disk[i]) + len(disk[i + 1]))
                        del disk[i]
                        del disk[i]
                        disk.insert(i, new_block)
                        i -= 1
                    i += 1
                break

    return [x for y in disk for x in y]


def calculate_checksum(disk: list[str]) -> int:
    """
    Calculate the checksum of the disk by summing the product of the index
    and the ID value of each block.

    Args:
        disk (str): The disk to calculate the checksum of.

    Returns:
        int: The checksum of the disk.
    """

    checksum = 0
    for i in range(len(disk)):
        if disk[i] != ".":  # Skip free space blocks
            checksum += i * int(disk[i])
    return checksum


def preprocess_input(input_text: list[str]):
    return input_text


def first(disk: str) -> int:
    disk = expand_disk(disk)
    disk = sort_disk_one_by_one(disk)
    return calculate_checksum(disk)


@print_timing
def second(disk: str) -> int:
    disk = expand_disk(disk, nested=True)
    disk = sort_disk_file_by_file(disk)
    return calculate_checksum(disk)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=9, year=2024)
    preprocessed_input = preprocess_input(original_input)

    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
