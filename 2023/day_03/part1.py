from machine import Machine

m = Machine(open('input.txt'))
total = sum(m)
print(f"Sum of part numbers: {total}")
