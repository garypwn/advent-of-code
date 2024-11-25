from modules import *

b = create_state_machine()
for _ in range(1000):
    press_button(b)

high, low = 0, 0
for m in modules.values():
    high += m.counter[Signal.HIGH]
    low += m.counter[Signal.LOW]

print(f"Final counts: {low} low, {high} high.")
print(f"Product: {high * low}")