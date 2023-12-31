from bricks import Brick, FallingBricks

b = FallingBricks(open("input.txt"))
b.settle_bricks()
print(f"{len(list(b.disintegratable_bricks()))} bricks can be safely disintegrated.")
