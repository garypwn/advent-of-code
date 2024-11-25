from rocks import *

p = parse(open('input.txt'))
roll(p, 'N')
print(f"Platform load: {load(p)}")

p = parse(open('input.txt'))
predict(p, 1000000000)
print(f"Platform load after 1000000000 spins: {load(p)}")
