from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 6)

def markers(s, size):
    indices = []
    for i, _ in enumerate(s):
        if len(set(s[i:i+size])) == size:
            indices.append(i+size)
    return indices

@puzzle.solution_a
def first_marker(data):
    return markers(data, 4)[0]

@puzzle.solution_b
def first_marker_p2(data):
    return markers(data, 14)[0]

puzzle.check_examples()
puzzle.check_solutions()