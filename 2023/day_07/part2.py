from camel import *

hands = read_lines(open('input.txt'), True)
hands.sort()
winnings = [hand.bid * (i+1) for i, hand in enumerate(hands)]
print(f"Total winnings: {sum(winnings)}")
