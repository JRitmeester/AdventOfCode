import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from pprint import pprint
import imageio.v2 as imageio

# Is it octopi, octopuses or something else? In this house, it is octos.
# There is a GIF export in here, but I'm not entirely sure the result is correct.
# The answers are correct, though.


def create_gif(image_folder: Path, name: str):
    images = [imageio.imread(file) for file in image_folder.glob("*.png")]
    imageio.mimsave(image_folder / name, images)


def save_image(image_arr, folder, name):
    plt.imshow(image_arr)
    plt.savefig(folder / name)
    plt.close()


def step(octos):
    # Add a charge to all octos.
    octos += 1

    # Keep track of octos that have already flashed.
    has_flashed = np.zeros_like(octos, dtype=np.bool)

    # Find the positions of octos with a charge above 9.
    charged_octos = list(zip(*np.nonzero(octos > 9)))

    flashes = 0

    while True:
        for y, x in charged_octos:
            if not has_flashed[y, x]:
                # Add a charge to the 3x3 neighbourhood.
                octos[max(y - 1, 0) : y + 2, max(x - 1, 0) : x + 2] += 1
                has_flashed[y, x] = True
                flashes += 1

        # Check for octos that are now charged.
        charged_octos = list(zip(*np.nonzero(np.multiply(octos, ~has_flashed) > 9)))

        # If no charged octos are found, quit.
        if len(charged_octos) == 0:
            break

    # Set the discharged octos to 0.
    octos = np.multiply(octos, ~has_flashed)
    return octos, flashes


def get_octos(input_raw):
    return np.array(
        [[int(energy) for energy in line] for line in input_raw.split("\n")]
    )


def main():
    cwd = Path(__file__).parent
    input_raw = (cwd / "input.txt").read_text()
    octos = get_octos(input_raw)

    # Part 1
    # Set up extra stuff to export the images to make a GIF from it.
    # It looks pretty cool! (Takes a little while though).
    make_gif = False
    folder = cwd / "images_part_1"
    if make_gif:
        folder.mkdir(exist_ok=True)
        save_image(octos, folder, "0.png")

    # Start simulating the flashes for 100 steps.
    total = 0
    for i in range(100):
        octos, flashes = step(octos)
        if make_gif:
            save_image(octos, folder, f"{i+1}.png")
        total += flashes

    print("Answer part 1:", total)

    if make_gif:
        create_gif(folder, "part1.gif")

    # Part 2

    # Reset the octos (you could continue from step 100 but that just
    # get confusing to me...
    octos = get_octos(input_raw)

    make_gif = True
    folder = cwd / "images_part_2"
    if make_gif:
        folder.mkdir(exist_ok=True)
        save_image(octos, folder, "0.png")

    steps = 0
    while True:
        steps += 1
        octos, _ = step(octos)

        if make_gif:
            save_image(octos, folder, f"{steps}.png")

        if np.sum(octos) == 0:
            break

    print("Answer part 2:", steps)
    create_gif(folder, "part2.gif")


if __name__ == "__main__":
    main()
