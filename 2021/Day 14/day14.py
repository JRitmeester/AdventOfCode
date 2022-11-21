import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint


def insert_char(base, insertion, i):
    return base[:i] + insertion + base[i:]


def grow_polymer(template, manual):
    """
    Go through the template, grab the pairs sequentially and insert the insertion element.
    """

    # Make a copy so the original stays available.
    copy = template

    for i in range(len(template) - 1):
        pair = template[i : i + 2]
        insertion = manual[pair]
        copy = insert_char(copy, insertion, (2 * i) + 1)
    return copy


def grow_polymer_better(pair_counts, manual):
    # Make a copy so the original stays available.
    copy = pair_counts.copy()

    # Record the creation of the new elements.
    new = {}

    for pair, count in pair_counts.items():
        insertion = manual[pair]  # Look up the insertion for this pair
        new[insertion] = (
            new.get(insertion, 0) + count
        )  # Record the count for this insertion.

        # Turn the pair (A, B) with insertion C into pairs AC and CB, and add `count` to the times that pair is present.
        pair_A = pair[0] + insertion
        pair_B = insertion + pair[1]
        copy[pair_A] = copy.get(pair_A, 0) + count
        copy[pair_B] = copy.get(pair_B, 0) + count

        # Remove `count` from the current pair's count because they have been broken up.
        copy[pair] -= count

    # Filter out the pairs with no occurrences left for cleanliness.
    return {pair: count for pair, count in copy.items() if count > 0}, new


def get_pair_counts(template):
    pair_counts = {}
    for i in range(len(template) - 1):
        pair = template[i : i + 2]
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    return pair_counts


def get_template_and_rules():
    input_raw = (Path(__file__).parent / "input.txt").read_text()
    template, rules = input_raw.split("\n\n")
    rules = rules.split("\n")
    return template, rules


def main():
    template, rules = get_template_and_rules()
    manual = dict([tuple(rule.split(" -> ")) for rule in rules])

    # Part 1
    # The intuitive approach: repeatedly grow the polymer by inserting the insertion base within the appropriate pairs.
    for i in range(10):
        template = grow_polymer(template, manual)

    # Count the occurrences of each letter.
    char_counts = {char: template.count(char) for char in set(template)}
    print("Answer part 1:", max(char_counts.values()) - min(char_counts.values()))

    # Part 2
    # The better approach: Count the pairs, and calculate the new pairs based on the new insertions.

    # Reset the template polymer.
    template = get_template_and_rules()[0]

    # Count the pairs in the beginning.
    pair_counts = get_pair_counts(template)

    # Count the elements occurrences in the beginning.
    element_count = {char: template.count(char) for char in set(template)}

    # "Grow" the polymer 40 times. Note that there is no way (afaik) to actually represent the polymer, since
    # the pair order is lost.
    for i in range(40):
        pair_counts, new_element_count = grow_polymer_better(pair_counts, manual)

        # Add all the newly added insertions to the counts that we already had.
        for element, count in new_element_count.items():
            element_count[element] = element_count.get(element, 0) + count

    print("Answer part 2:", max(element_count.values()) - min(element_count.values()))


if __name__ == "__main__":
    main()
