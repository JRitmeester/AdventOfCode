import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Add the repository root the sys.path in order to import the helper modules.
file = Path(__file__)
REPO_ROOT = next(
    (parent for parent in file.parents if parent.name.lower() == "advent of code"),
    None,
)
sys.path.append(REPO_ROOT.as_posix())
from aoc_util.helpers import load_input_data, print_timing


def preprocess_input(input_text: str, size=(99, 99)):
    return np.array(
        [int(n) for line in "".join(input_text.split("\n")) for n in line]
    ).reshape(size)

def get_visible_trees(trees):


    def get_visible_trees_from_direction(
        trees: np.ndarray, rot90_n_times: int
    ) -> np.ndarray:
        trees = np.rot90(trees, k=rot90_n_times)

        """
        Loop through the columns on the forest and find for each tree if it is behind a taller tree.
        For each tree location, the height of the tallest  tree so far is propagated onto the rest of the column until
        a taller tree is found, and so on. The points where this height changes is where a new tree becomes visible.
        The forest matrix may be rotated so that the same approach can be applied to find the visible trees from the 
        north (k=0), east (k=1), south (k=2), or west (k=3).
        """
        min_height_for_visibility = np.zeros_like(trees)
        for x, column in enumerate(trees.T):
            min_height = 0
            for y, tree in enumerate(column):
                if tree > min_height:
                    min_height = tree
                min_height_for_visibility[y][x] = min_height
        visible_trees = np.rot90(
            np.diff(min_height_for_visibility, axis=0, prepend=-1) > 0, k=-rot90_n_times
        )

        return visible_trees
    
    visible_trees = sum(get_visible_trees_from_direction(trees, rot90_n_times=i) for i in range(4)) > 0
    return visible_trees

def get_scenic_score(trees, x, y):
    north_view = trees[:y, x][::-1]
    east_view = trees[y, x + 1 :]
    south_view = trees[y + 1 :, x]
    west_view = trees[y, :x][::-1]
    
    hut_height = trees[y,x]
    trees_per_dir = []
    
    for view_dir in [north_view, east_view, south_view, west_view]:
        if view_dir.size == 0:  # If you're on the edge of the forest.
            n_visible_trees = 0
            continue
        
        # Find how many trees it takes before one blocks your view (including that tree)
        height_diff = view_dir - hut_height
        for i, diff in enumerate(height_diff,1):
            if diff >= 0:
                trees_per_dir.append(i)
                break
        else:
            trees_per_dir.append(len(view_dir))

    return np.prod(trees_per_dir)
    

@print_timing
def first(trees) -> int:
    visible_trees = get_visible_trees(trees)
    return np.sum(visible_trees)


@print_timing
def second(trees) -> int:
    invisible_trees = ~get_visible_trees(trees)
    scencic_scores = [
        get_scenic_score(trees, x, y) for x, y in zip(*np.nonzero(invisible_trees))
    ]
    return max(scencic_scores)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=8, year=2022)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
