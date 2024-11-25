from math import lcm

from desert import *

path, network = read_lines(open('input.txt'))
lengths = find_repetitions(path, network)
print([length[2] for length in lengths])

result = lcm(*[length[0] for length in lengths])

print(f"Path length is: {result}")
