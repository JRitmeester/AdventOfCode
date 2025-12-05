from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from pprint import pprint
from typing import List, Tuple

RangesType = List[Tuple[int, int]]
IDsType = List[int]


def preprocess_input(input_text: str) -> tuple[RangesType, IDsType]:
    ranges, ids = input_text.split("\n\n")
    print(ranges)
    ranges_clean = []
    for range in ranges.split("\n"):
        start, stop = range.split("-")
        ranges_clean.append((int(start), int(stop)))
    ids_clean = [int(x) for x in ids.split("\n")]
    return ranges_clean, ids_clean


def get_fresh_and_spoiled(
    ranges: RangesType, ids: IDsType
) -> tuple[set[int], set[int]]:
    fresh = []
    spoiled = []
    for id in ids:
        for start, stop in ranges:
            if start <= id <= stop:
                fresh.append(id)
            else:
                spoiled.append(id)
    return set(fresh), set(spoiled)


def merge_overlapping_ranges(ranges: RangesType) -> RangesType:
    """
    Sort ranges by start, then merge if current_end + 1 >= next_start

    ======........===.....========.====....====
    s    e        s e     s      e s  e    s  e

    +

    ....======.....====.=====.....=======...===
        s    e     s  e s   e     s     e   s e

    =

    ==========....=====.=================..====
    s        e    s   e s               e  s  e
    """

    # Sort ranges by start value
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    merged = [sorted_ranges[0]]

    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # If ranges overlap or are adjacent (end + 1 >= start), merge them
        if last_end + 1 >= start:
            # Merge: extend the end to the maximum of both ends
            merged[-1] = (last_start, max(last_end, end))
        else:
            # No overlap, add as new range
            merged.append((start, end))

    return merged


def count_valid_ids(ranges: RangesType) -> int:
    """
    Count the total number of unique valid IDs across all ranges.
    """
    merged = merge_overlapping_ranges(ranges)
    return sum(end - start + 1 for start, end in merged)


def get_all_fresh_ids(ranges: RangesType) -> int:
    """
    Get all valid IDs in the merged ranges.
    """
    merged = merge_overlapping_ranges(ranges)
    valid_ids = set()
    for start, end in merged:
        valid_ids.update(range(start, end + 1))
    return valid_ids


def first(ranges: RangesType, ids: IDsType) -> int:
    fresh_ids, spoiled_ids = get_fresh_and_spoiled(ranges, ids)
    print(fresh_ids)
    return len(fresh_ids)


def second(ranges: RangesType, ids: IDsType) -> int:
    return count_valid_ids(ranges)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=5, year=2025)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(*preprocessed_input))
    print("The answer to part 2 is:", second(*preprocessed_input))
