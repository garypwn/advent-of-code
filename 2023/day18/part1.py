from trench import *

pt, t = parse(open('input.txt'))
flood_fill(t, (1, -1))
print(len(t))
