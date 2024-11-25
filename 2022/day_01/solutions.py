from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 1)

def sum_calories(data: str):
    elves = [0]
    for line in data.split("\n"):
        if line == "":
            elves.append(0)
        else:
            elves[-1] += int(line)

    return elves

@puzzle.solution_a
def max_cal(data):
    elves = sum_calories(data)
    return max(elves)

@puzzle.solution_b
def top_three(data):
    elves = sum_calories(data)
    elves.sort()
    return sum(elves[-1:-4:-1])

puzzle.check_examples()
puzzle.check_solutions()