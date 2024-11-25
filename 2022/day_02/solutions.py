from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 2)

# Maps ABCXYZ to rock paper scissors point values.
RPS_VALUES = {
    #Rock
    'A': 1,
    'X': 1,

    #Paper
    'B': 2,
    'Y': 2,

    #Scissors
    'C': 3,
    'Z': 3
}

# We can figure out the result of a match really easily with modular arithmetic.
# X - Y mod 3 gives the result. 0 is a draw, 1 is a win, 2 is a loss.

def score(opponent, player):
    result = (RPS_VALUES[player] - RPS_VALUES[opponent] + 10) % 3
    return result * 3 + RPS_VALUES[player]

@puzzle.solution_a
def total_score(data):
    scores = [score(line[0], line[2]) for line in data.split('\n')]
    return sum(scores)

XYZ_VALUES = {
    'X': 0,
    'Y': 1,
    'Z': 2
}

def score_p2(opp, outcome):
    player = (RPS_VALUES[opp] + XYZ_VALUES[outcome] - 1) % 3
    if player == 0:
        player = 3
    return player + 3 * XYZ_VALUES[outcome]

@puzzle.solution_b
def total_p2(data):
    scores = [score_p2(line[0], line[2]) for line in data.split('\n')]
    return sum(scores)

puzzle.check_examples()
puzzle.check_solutions()
