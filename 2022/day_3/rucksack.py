from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 3)

def priority(s) -> int:
    if s.islower():
        return ord(s) - 96
    else:
        return ord(s) - 38

def find_item(line) -> str:
    container = set()
    for s in line[:len(line)//2]:
        container.add(s)

    for s in line[len(line)//2:]:
        if s in container:
            return s

@puzzle.solution_a
def sum_priorities(data):
    return sum([priority(find_item(line)) for line in data.split('\n')])

def find_badge(elves):
    b = set(elves[0]) & set(elves[1]) & set(elves[2])
    assert len(b) == 1
    return b.pop()

@puzzle.solution_b
def sum_badges(data):
    lines = data.split('\n')
    groups = [lines[i:i+3] for i in range(0, len(lines), 3)]
    return sum([priority(find_badge(group)) for group in groups])

puzzle.check_examples()
puzzle.check_solutions()