from holiday_hash import *

result = sum((holiday_hash(s.strip()) for s in open('input.txt').read().split(',')))
print(f"Part 1: Sum of instruction hashes: {result}")

boxes = initialization(open('input.txt').read())
print(f"Part 2: Sum of focusing powers: {sum(boxes.powers())}")