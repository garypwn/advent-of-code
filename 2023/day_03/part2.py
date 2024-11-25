from machine import Machine

m = Machine(open('input.txt'))
ratios = sum([p1 * p2 for p1, p2 in m.gears()])
print(f"Sum of gear powers: {ratios}")
