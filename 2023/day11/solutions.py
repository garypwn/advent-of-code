from universe import *

universe = expand(expand(parse(open('input.txt')), 1), 0)

print(f"Sum of shortest paths: {solve_p1(universe)}")