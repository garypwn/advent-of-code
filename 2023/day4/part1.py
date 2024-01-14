from scratchcard import *

cards = read_lines(open('input.txt'))
total = sum(points(*card) for card in cards)
print(f"Sum of points is {total}")