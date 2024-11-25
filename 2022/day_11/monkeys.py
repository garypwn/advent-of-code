import re

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 11)


class Monkey:
    def __init__(self, monkey_list: list, operation: tuple[int, int] | str, test: int, targets: tuple[int, int],
                 items=None):
        self.monkey_list = monkey_list
        if items is None:
            items = []
        self.items = items
        self.targets = targets
        self.operation = operation
        self.test = test
        self.inspection_count = 0

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
            item //= 3

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
def monkey_business(data, rounds=20):
    monkeys = parse_data(data)
    for _ in range(rounds):
        for monkey in monkeys:
            for _ in monkey.take_turn():
                pass

    activity = [monkey.inspection_count for monkey in monkeys]
    activity.sort(reverse=True)
    return activity[0] * activity[1]


puzzle.check_examples()
puzzle.check_solutions()