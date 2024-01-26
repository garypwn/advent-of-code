import cProfile

from workflows import *

print(f"Part 1: Sum of accepted parts: {solve(open('input.txt'))}")
pr = cProfile.Profile()
pr.enable()
print(f"Part 2: Number of distinct accepted parts: {solve_p2(open('input.txt'))}")
pr.disable()
pr.dump_stats('out.prof')
