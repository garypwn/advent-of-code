from springs import *

lines = parse(open('input.txt'))
print(f"Sum of arrangement counts: {sum([arrangements(*line) for line in lines])}")

lines = unfold(parse(open('input.txt')))
print(f"Sum of arrangement counts in unfolded record: {sum([arrangements(*line) for line in lines])}")
