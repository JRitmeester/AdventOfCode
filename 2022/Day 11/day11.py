from pathlib import Path; file = Path(__file__); import sys; sys.path.append(file.parents[2].as_posix())  # fmt: skip
from aoc_util.helpers import load_input_data

import numpy as np
from dataclasses import dataclass


@dataclass
class Monkey:
    id: int  # The ID of the monkey
    items: list[int]  # The worry values of the items the monkey currently has
    test: int  # The value by which to divide to see to which monkey the item will be thrown
    true_id: int  # The number of the monkey to which the item is thrown if test is True
    false_id: int  # The number of the monkey to which the item is thrown if test if False
    operation: str  # The numerical operation to get new worry level
    inspections: int = 0  # The number of times

    def __post_init__(self):
        self.operation = lambda old, op=self.operation: eval(op)

    def __repr__(self):
        return f"<Monkey {self.id}, with items {self.items}>"


def keep_away(monkeys: list[Monkey], rounds: int, relief: bool):
    # Something something number theory. Congruency, coprimes, modulo. Abracadabra. Thanks Reddit.
    monkey_test_prod = np.prod([monkey.test for monkey in monkeys])

    for _ in range(rounds):
        for m in monkeys:
            for worry_level in m.items:
                m.inspections += 1
                new_level = m.operation(worry_level) // 3 if relief else m.operation(worry_level)  # fmt:skip
                to_monkey = m.false_id if new_level % m.test else m.true_id
                monkeys[to_monkey].items.append(new_level % monkey_test_prod)  # fmt:skip
            m.items = []  # All items are thrown to other monkeys
    return monkeys


def preprocess_input(input_text: str):
    monkeys = [
        Monkey(
            id=int(a[7:-1]),
            items=[int(n) for n in b[18:].split(", ")],
            operation=c[19:],
            test=int(d[21:]),
            true_id=int(e[29:]),
            false_id=int(f[30:]),
        )
        for a, b, c, d, e, f in [m.split("\n") for m in input_text.split("\n\n")]
    ]
    return monkeys


def first(monkeys: list[Monkey]) -> int:
    monkeys = keep_away(monkeys, 20, relief=True)
    monkey_inpsections = sorted([monkey.inspections for monkey in monkeys])
    return monkey_inpsections[-1] * monkey_inpsections[-2]


def second(monkeys: list[Monkey]) -> int:
    monkeys = keep_away(monkeys, 10_000, relief=False)
    monkey_inpsections = sorted([monkey.inspections for monkey in monkeys])
    return monkey_inpsections[-1] * monkey_inpsections[-2]


if __name__ == "__main__":
    original_input = load_input_data(file.parent / "input.txt", day=11, year=2022)
    preprocessed_input = preprocess_input(original_input)
    print("The answer to part 1 is:", first(preprocessed_input))
    print("The answer to part 2 is:", f"{second(preprocessed_input):_}")
