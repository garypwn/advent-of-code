from universe import *

universe = expand(expand(parse(open('input.txt')), 1), 0)
print(f"Sum of shortest paths in 2-expanded universe: {solve(universe, 2)}")
print(f"Sum of shortest paths in million-expanded universe : {solve(universe, 1000000)}")
