import string


def first_digit(seq):
    for c in seq:
        if c in string.digits:
            return c


def extract_number(seq: str):
    first = first_digit(seq)
    last = first_digit(seq[::-1])

    n = int(f"{first}{last}")
    return n


values = []
for line in open("input.txt"):
    values.append(extract_number(line))

print(f"Sum of calibration values: {sum(values)}")
