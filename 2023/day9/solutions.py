from oasis import *

predictions = [predict(nums) for nums in parse(open('input.txt'))]

print(f"Part 1 predictions: {predictions}")
print(f"Sum: {sum(predictions)}")

print()

predictions = [predict_left(nums) for nums in parse(open('input.txt'))]

print(f"Part 2 predictions: {predictions}")
print(f"Sum: {sum(predictions)}")
