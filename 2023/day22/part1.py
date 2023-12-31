from bricks import FallingBricks

b = FallingBricks(open("input.txt"))
print(f"Dropping {len(b.bricks)} bricks.")
ct = b.settle_bricks()
print(f"All bricks are supported after {ct} steps.\n")
print(f"{len(list(b.disintegratable_bricks()))} bricks can be safely disintegrated.")
