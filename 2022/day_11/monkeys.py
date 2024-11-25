import re
from math import lcm

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 11)


class Monkey:
    def __init__(self, monkey_list: list, operation: tuple[int, int] | str, test: int, targets: tuple[int, int],
                 items=None, stress_relief=True):
        self.monkey_list = monkey_list
        if items is None:
            items = []
        self.items = items
        self.targets = targets
        self.operation = operation
        self.test = test
        self.inspection_count = 0
        self.stress_relief = stress_relief
        self.magic_number = None

    def add_item(self, item):
        self.items.append(item)

    def take_turn(self):
        items = self.items
        self.items = []
        for item in items:

            # Inspect
            if self.operation == "square":
                item *= item
            else:
                mult, add = self.operation
                item = item * mult + add
            self.inspection_count += 1
            yield item
            if self.stress_relief:
                item //= 3
            elif self.magic_number:
                item %= self.magic_number

            if item % self.test == 0:
                target = self.monkey_list[self.targets[0]]
            else:
                target = self.monkey_list[self.targets[1]]
            target.add_item(item)


def parse_data(data):
    monkeys = []
    pattern = re.compile(r"Monkey \d+:\s.*Starting items: (.*)\s.*([*|+]) (.+)\s.* (\d+)\s.* (\d+)\s.* (\d+)")
    for block in data.split('\n\n'):
        items, operator, operand, test, t1, t2 = pattern.match(block).groups()

        if operand == "old":
            op = "square"
        else:
            op = (int(operand), 0) if operator == "*" else (1, int(operand))

        monkeys.append(Monkey(
            monkeys,
            op,
            int(test),
            (int(t1), int(t2)),
            [int(item) for item in items.split(', ')]
        ))
    return monkeys


@puzzle.solution_a
def monkey_business(data, rounds=20, stress_relief=True):
    monkeys = parse_data(data)

    # The trick to part B is this magic number. The main roadblock for doing 100000 rounds is the integer valued
    # stress levels getting prohibitively large. Since each monkey's test condition is a modulo operation, we can just
    # use the LCM of all the monkeys' test conditions, and %= the stress values each turn.
    magic_number = lcm(*(monkey.test for monkey in monkeys))

    for monkey in monkeys:
        monkey.stress_relief = stress_relief
        monkey.magic_number = magic_number

    for _ in range(rounds):
        for monkey in monkeys:
            for _ in monkey.take_turn():
                pass

    activity = [monkey.inspection_count for monkey in monkeys]
    activity.sort(reverse=True)
    return activity[0] * activity[1]


@puzzle.solution_b
def monkey_business_p2(data):
    return monkey_business(data, 10000, False)


puzzle.check_examples()
puzzle.check_solutions()
