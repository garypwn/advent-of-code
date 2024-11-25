import re

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 5)

def parse(data: str):
    """
    Returns (boxes, instructions). Boxes is a list of lists, where the outer list is 1-indexed.
    Stacks of boxes are in order from bottom to top.

    Instructions is a list of (count, source, dest).
    """

    p1, p2 = data.split('\n\n')

    # Parse boxes.
    boxes = [[] for _ in range(int(p1.strip()[-1]))]
    for line in p1.split('\n')[-2::-1]:
        for i, box in enumerate(boxes):
            if line[1+4*i].isalpha():
                box.append(line[1+4*i])

    # Make it 1-indexed by adding an empty list at the start
    boxes = [[]] + boxes

    # Parse instructions
    pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
    instructions = [(int(group) for group in pattern.match(line).groups()) for line in p2.split('\n')]

    return boxes, instructions

def top_boxes(data, p2=False):
    boxes, instructions = parse(data)

    for count, source, dest in instructions:
        boxes[source], x = boxes[source][:-count], boxes[source][-count:]
        boxes[dest] += x if p2 else x[::-1]

    result = ""
    for stack in boxes[1:]:
        if stack[-1]:
            result += stack[-1]

    return result

@puzzle.solution_a
def solve_p1(data):
    return top_boxes(data)

@puzzle.solution_b
def solve_p2(data):
    return top_boxes(data, True)

puzzle.check_examples()
puzzle.check_solutions()