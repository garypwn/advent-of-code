from scratchcard import *

cards = read_lines(open('input.txt'))
count = play(cards)
print(f"Total number of cards: {count}")