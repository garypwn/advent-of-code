from collections.abc import Iterable
from itertools import pairwise

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 9)


def parse(data):
    # Iterate over the input as (addr, size, value) blocks of contiguous data
    ptr = 0
    for i, ct in enumerate((int(s) for s in data)):
        if i % 2 == 1:
            yield ptr, ct, None
        else:
            yield ptr, ct, i // 2
        ptr += ct


def compress(disk: Iterable):
    # Iterate over the compressed disk
    disk = list(disk)
    addr, rem, val = disk.pop()  # Our filler file from the end of the list
    while disk:
        addr, sz, block_val = disk.pop(0)

        if block_val is not None:
            yield addr, sz, block_val

        else:

            if not disk:
                break

            # Fill in empty space
            while sz > 0:

                # Refill our filler
                while rem == 0 or val is None:
                    if not disk:
                        return
                    _, rem, val = disk.pop()

                n = min(rem, sz)
                sz -= n
                rem -= n

                yield addr, n, val
                addr += n

    if rem > 0:
        yield addr, rem, val

def compress_p2(disk: Iterable):
    # Iterate over the compressed disk without fragmenting files

    disk = [[addr, sz, val] for addr, sz, val in disk if val is not None]

    def flat(blocks):
        # Flat iterate over nested lists
        for block in blocks:
            if not block:
                continue
            if isinstance(block[0], list):
                for b in flat(block):
                    yield b
            else:
                yield block

    # Keep a data structure holding the earliest gaps, since the max size is 9
    gaps = {x: None for x in range(10)}

    # Iterate over files in reverse
    for file in disk[-1:0:-1]:
        # If this file is a combo node, we can unwrap it
        while isinstance(file[0], list):
            file = file[0]

        addr, sz, val = file

        # Iterate over pairs of files to find gaps
        for before, after in pairwise(flat(disk)):
            b_addr, b_sz, b_val = before
            if b_addr > addr or b_val == val:
                break

            space = after[0] - b_addr - b_sz
            if space >= sz:
                before.clear()
                before += [[b_addr, b_sz, b_val], [b_addr+b_sz, sz, val]]
                file.clear()
                break

    return flat(disk)

def checksum(disk: Iterable):
    def it():
        for addr, sz, val in disk:
            if val is None:
                continue
            for i in range(sz):
                yield val * (addr + i)

    return sum(it())


@puzzle.solution_a
def solve_p1(data):
    disk = compress(parse(data))
    disk = list(disk)
    return checksum(disk)

@puzzle.solution_b
def solve_p2(data):
    disk = compress_p2(parse(data))
    return checksum(disk)


puzzle.check_examples()
puzzle.check_solutions()
