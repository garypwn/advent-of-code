from oasis import *

predictions = []
for nums in parse(open('input.txt')):
    predictions.append(predict(nums))

print(f"Predictions: {predictions}")
print(f"Sum: {sum(predictions)}")
