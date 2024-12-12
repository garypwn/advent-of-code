from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 11)


def parse(data):
    l = [int(s) for s in data.split(' ')]
    return {s: l.count(s) for s in l}


def blink(stones):
    new = {1: 0}
    for stone, ct in stones.items():
        if stone == 0:
            new[1] += ct
            continue

        s = str(stone)
        if len(s) % 2 == 0:
            split = int(s[:len(s) // 2]), int(s[len(s) // 2:])
            for p in split:
                if p in new:
                    new[p] += ct
                else:
                    new[p] = ct
        else:
            new[stone * 2024] = ct

    return new


@puzzle.solution_a
def solve_p1(data, ct=25):
    stones = parse(data)
    for _ in range(ct):
        stones = blink(stones)
    return sum(stones.values())

@puzzle.solution_b
def solve_p2(data):
    return solve_p1(data, 75)



puzzle.check_solutions()