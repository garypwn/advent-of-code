from rocks import *

p = parse(open('input.txt'))
roll(p, 'N')
print(f"Platform load: {load(p)}")
