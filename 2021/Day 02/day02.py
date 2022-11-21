from pathlib import Path


class Submarine:
    def __init__(self, use_aim: bool):
        self.pos = 0
        self.depth = 0
        self.aim = 0
        self.use_aim = use_aim

    def forward(self, x):
        self.pos += x
        if self.use_aim:
            self.depth += self.aim * x

    def up(self, x):
        if self.use_aim:
            self.aim -= x
        else:
            self.depth -= x

    def down(self, x):
        self.up(-x)

    def parse_instructions(self, instructions):
        for line in instructions:
            command, amount = line.split(" ")

            # Not very clean, but cooler than if statements.
            getattr(self, command)(int(amount))


def main():
    instructions_path = Path(__file__).parent / "input.txt"
    with instructions_path.open(mode="r") as file:
        instructions = file.readlines()

    # Part 1
    sub = Submarine(use_aim=False)
    sub.parse_instructions(instructions)
    print("Answer 1: ", sub.pos * sub.depth)

    # Part 2
    sub = Submarine(use_aim=True)
    sub.parse_instructions(instructions)
    print("Answer 2: ", sub.pos * sub.depth)


if __name__ == "__main__":
    main()
