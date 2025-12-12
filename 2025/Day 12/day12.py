from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import re
from concurrent.futures import ProcessPoolExecutor


def preprocess_input(input_text: str):
    """Parse shapes and regions from input."""
    # Parse shapes into 3x3 grids, each preceded by a number and colon
    shape_blocks = re.findall(r"\d+:\n(?:[#.]+\n?)+", input_text)
    shapes = []
    for block in shape_blocks:
        # Remove the leading line with the shape number/colon
        block_rows = block.split("\n")[1:]
        # Ignore any empty rows (may occur at the end)
        block_rows = [row for row in block_rows if row]
        # Make a numpy array where '#' is 1 and '.' is 0
        arr = []
        for row in block_rows:
            arr.append([c == "#" for c in row])
        shapes.append(np.array(arr, dtype=int))

    # Parse regions, e.g., "12x5: 1 0 1 0 2 2" -> ((12, 5), [1, 0, 1, 0, 2, 2])
    region_matches = re.findall(r"(\d+)x(\d+): ([\d ]+)", input_text)
    regions = []
    for w, h, counts in region_matches:
        width = int(w)
        height = int(h)
        count_list = [int(x) for x in counts.split()]
        regions.append(((width, height), count_list))

    return shapes, regions


def get_all_isometries(shape: np.ndarray):
    """Get all unique rotations and reflections of a shape."""
    R = lambda s, k: np.rot90(s, k)
    V, H = np.flipud, np.fliplr

    candidates = [
        shape,
        R(shape, 1),
        R(shape, 2),
        R(shape, 3),
        V(shape),
        H(shape),
        R(V(shape), 1),
        R(H(shape), 1),
    ]
    unique = []
    for iso in candidates:
        if not any(np.array_equal(iso, u) for u in unique):
            unique.append(iso)
    return unique


def shape_to_cells(shape: np.ndarray) -> tuple:
    """Convert shape to tuple of (row, col) coordinates where cells are filled."""
    return tuple(
        (r, c)
        for r in range(shape.shape[0])
        for c in range(shape.shape[1])
        if shape[r, c]
    )


def can_fit(
    presents: list, isometries: list, w: int, h: int, node_limit: int = 10000
) -> bool:
    """Iterative DFS with explicit stack and set-based collision detection."""
    if not presents:
        return True

    grid = set()
    nodes = 0

    # Stack entries: (present_idx, placement_iterator, placed_cells_or_None)
    # We use a generator for each level to iterate through all placement options
    def placement_options(idx):
        """Generator yielding all valid placements for present at idx."""
        for cells, iso_h, iso_w in isometries[presents[idx]]:
            for row in range(h - iso_h + 1):
                for col in range(w - iso_w + 1):
                    yield {(r + row, c + col) for r, c in cells}

    # Initialize stack with first present
    stack = [(0, placement_options(0), None)]

    while stack:
        nodes += 1
        if nodes > node_limit:
            return False

        idx, options, last_placed = stack[-1]

        # Backtrack: remove what was placed at this level (if anything)
        if last_placed is not None:
            grid.difference_update(last_placed)

        # Try next placement option at this level
        for placed in options:
            if not (placed & grid):  # No collision
                grid.update(placed)
                stack[-1] = (idx, options, placed)  # Remember what was placed

                if idx + 1 >= len(presents):
                    return True  # All presents placed!

                # Push next present onto stack
                stack.append((idx + 1, placement_options(idx + 1), None))
                break
        else:
            # No more options at this level, pop and backtrack
            stack.pop()

    return False


def check_region(args):
    """Check if a single region can fit all its presents."""
    (w, h), counts, isometries, cell_counts, num_shapes = args
    counts = (counts + [0] * num_shapes)[:num_shapes]

    # Build present list and sort by size (largest first)
    presents = [i for i, cnt in enumerate(counts) for _ in range(cnt)]
    presents.sort(key=lambda i: -cell_counts[i])

    # Early prune: check if total area fits
    if sum(cell_counts[i] for i in presents) > w * h:
        return False

    # Try to fit all presents using iterative DFS
    return can_fit(presents, isometries, w, h)


def first(shapes, regions) -> int:
    # Precompute isometries as (cells, height, width) tuples
    isometries = [
        [
            (shape_to_cells(iso), iso.shape[0], iso.shape[1])
            for iso in get_all_isometries(shape)
        ]
        for shape in shapes
    ]
    cell_counts = [len(isometries[i][0][0]) for i in range(len(shapes))]

    # Prepare args for parallel execution
    args = [
        ((w, h), counts, isometries, cell_counts, len(shapes))
        for (w, h), counts in regions
    ]

    # Run in parallel
    with ProcessPoolExecutor() as executor:
        results = executor.map(check_region, args)

    return sum(results)


def second(input_data) -> int:
    """Merry Christmas"""
    pass


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=12, year=2025)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(*preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
