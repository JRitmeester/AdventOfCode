from pathlib import Path
file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import *
import numpy as np
import multiprocessing as mp


# Define direction change mappings for each tile
mirrors = {
    '/': {'right': 'up', 'up': 'right', 'left': 'down', 'down': 'left'},
    '\\': {'up': 'left', 'left': 'up', 'right': 'down', 'down': 'right'}
}


class Ray:

    def __init__(self, pos: tuple[int, int], dir: str):
        self.pos = pos
        self.dir = dir

    def __repr__(self):
        return f"Ray [pos={tuple(self.pos)}, dir={self.dir}"
    
    def move(self):
        self.pos += DIRS[self.dir]

    def is_out_of_bounds(self, grid):
        return self.pos[0] < 0 or self.pos[0] >= grid.shape[0] or self.pos[1] < 0 or self.pos[1] >= grid.shape[1]
    
    def change_dir(self, dir: str):
        self.dir = dir

    @property
    def state(self):
        return (tuple(self.pos), self.dir)


def count_energised_tiles(grid: np.ndarray, start_x: int, start_y: int, start_dir: str, queue: mp.Queue=None) -> int:
    cache = []
    starting_ray = Ray(pos=np.array((start_y, start_x)), dir=start_dir)
    rays = [starting_ray]

    # Keep track of which tiles have already been energised
    is_energised = np.zeros(grid.shape, dtype=bool)

    while len(rays) > 0:
        for i, ray in enumerate(rays):
            ray.move()

            if ray.is_out_of_bounds(grid):
                rays.remove(ray)
                continue

            y, x = ray.pos
            dir = ray.dir
            tile = grid[y, x]

            # Change direction based on the tile
            if tile in mirrors and dir in mirrors[tile]:
                dir = mirrors[tile][dir]
                ray.change_dir(dir)
            elif tile == '|':
                if dir in ['left', 'right']:
                    ray.change_dir('up')
                    rays.append(Ray(pos=ray.pos.copy(), dir='down'))
            elif tile == '-':
                if dir in ['up', 'down']:
                    ray.change_dir('left')
                    rays.append(Ray(pos=ray.pos.copy(), dir='right'))

            # Handle ray state and caching
            if ray.state in cache:
                rays.remove(ray)
            else:
                is_energised[y, x] = True
                cache.append(ray.state)

    # Variable return types? Blasphemy!
    if queue is not None:
        queue.put(np.count_nonzero(is_energised))
    else:
        return np.count_nonzero(is_energised)


def preprocess_input(input_text: str):
    return create_numpy_grid(input_text)


def first(grid: np.ndarray) -> int:
    return count_energised_tiles(grid, -1, 0, "right")
    

def second(grid) -> int:
    starts = []
    max_y = grid.shape[0] - 1
    max_x = grid.shape[1] - 1
    for y in range(grid.shape[0]):
        starts.append((0, y, 'right'))
        starts.append((max_x, y, 'left'))

    for x in range(grid.shape[1]):
        starts.append((x, 0, 'down'))
        starts.append((x, max_y, 'up'))

    # Use multiprocessing because I am too lazy to optimise any of this further.
    # Unparallelised this takes about 10 minutes to run. For which I am also too lazy to wait.
    queue = mp.Queue()

    processes = []
    for x, y, dir in starts:
        p = mp.Process(target=count_energised_tiles, args=(grid, x, y, dir, queue))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
    
    values = [queue.get() for _ in processes]
    return max(values)


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=16, year=2023)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", second(preprocessed_input))
