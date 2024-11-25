import re

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 10)

def process_instructions(data):
    x = 1
    pattern = re.compile(r"addx (-?\d+)")
    for line in data.split('\n'):
        if line == "noop":
            yield x
        else:
            yield x
            yield x
            x += int(pattern.match(line).group(1))

@puzzle.solution_a
def solve_p1(data):
    total = 0
    for i, x in enumerate(process_instructions(data)):
        if i % 40 == 19:
            total += (i+1)*x
    return total

@puzzle.solution_b
def draw_p2(data):
    s = ""
    for i, x in enumerate(process_instructions(data)):
        if i % 40 == 0:
            s += '\n'
        if x-1 <= i % 40 <= x+1:
            s += '#'
        else:
            s+= '.'
    print(s)

puzzle.check_examples()
puzzle.check_solutions()