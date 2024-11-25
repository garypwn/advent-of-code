import math

from races import *

t, d = read_input_2(open('input.txt'))
roots = (-t + math.sqrt(t**2 - 4*d)) / -2., (-t - math.sqrt(t**2 - 4*d)) / -2.
low = math.ceil(min(roots))  # inclusive
high = math.ceil(max(roots))  # exclusive

print(f"Winning speed range: {low, high}")
print(f"Number of winning speeds: {high - low}")
