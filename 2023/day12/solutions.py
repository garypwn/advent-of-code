from springs import *

lines = parse(open('input.txt'))
print(f"Sum of arrangement counts: {sum([len(arrangements(*line)) for line in lines])}")
