from __future__ import annotations

from bricks import Brick, FallingBricks

trees: dict[Brick: BrickTree] = {}


def get_tree(brick: Brick):
    # Gets the dag rooted at this brick that represents all the bricks supported by it.
    # Recursion warning!!!!

    if brick in trees:
        return trees[brick]

    tree = BrickTree(brick)
    for child in brick.supporting:
        if child.supporters <= tree.members:
            tree.add_brick(child)
        else:
            tree.dead_ends.add(child)

    tree.revive(tree.dead_ends)
    trees[brick] = tree
    return tree


class BrickTree:
    root: Brick
    members: set[Brick]  # Includes root
    dead_ends: set[Brick]

    def __init__(self, root: Brick):
        self.root = root
        self.members = {root}
        self.dead_ends = set()

    def __contains__(self, item: Brick):
        return item in self.members

    def __len__(self):
        return len(self.members)

    def fall_count(self):
        return len(self) - 1

    def add_brick(self, brick):
        tree = get_tree(brick)
        self.members |= tree.members
        self.dead_ends |= tree.dead_ends - self.members
        self.revive(self.dead_ends & tree.dead_ends)

    def revive(self, contenders):
        # Rechecks dead ends and revives them if possible
        # Recursion danger
        for brick in list(contenders):
            if brick.supporters <= self.members:
                self.add_brick(brick)
                self.dead_ends.discard(brick)


bricks = FallingBricks(open("input.txt"))
print(f"Dropping {len(bricks.bricks)} bricks...")
print(f"All bricks are supported after {bricks.settle_bricks()} steps.\n")
bricks.bricks.sort(key=lambda x: x.bottom_height(), reverse=True)
print(f"Computing spanning trees for this {bricks.bricks[0].top_height()} brick high tower.")
for b in bricks.bricks:
    get_tree(b)

# Now add them up
total = 0
for t in trees.values():
    total += t.fall_count()

print(f"The sum of bricks that would fall is {total}")
