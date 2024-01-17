from races import *

races = read_input(open('input.txt'))

product = 1
for race in races:
    outcomes = (speed * (race[0] - speed) for speed in range(race[0]))
    winners = filter(lambda outcome: outcome > race[1], outcomes)
    product *= len(list(winners))

print(f"Product of winner counts: {product}")