import string

digits = {'one': 1,
          'two': 2,
          'three': 3,
          'four': 4,
          'five': 5,
          'six': 6,
          'seven': 7,
          'eight': 8,
          'nine': 9}


def starting_digit(seq):
    # Returns the digit at the very start of the char sequence, or None

    if seq[0] in string.digits:
        return seq[0]

    for digit in digits.keys():
        if seq[:len(digit)] == digit:
            return digits[digit]

    return None


def first_digit(seq, start=0, stride=1):
    stop = len(seq) if stride > 0 else -len(seq)
    for i in range(start, stop, stride):
        digit = starting_digit(seq[start + i:])
        if digit:
            return digit


def extract_number(seq: str):
    first = first_digit(seq)
    last = first_digit(seq, -1, -1)

    n = int(f"{first}{last}")
    return n


values = []
for line in open("input.txt"):
    values.append(extract_number(line))

print(f"Sum of calibration values: {sum(values)}")
