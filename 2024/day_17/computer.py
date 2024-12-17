from itertools import batched, chain

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 17)


def parse(data):
    lines = [line.split(' ') for line in data.split('\n')]
    return VM(int(lines[0][2]), int(lines[1][2]), int(lines[2][2])), [int(s) for s in lines[4][1].split(',')]


class VM:
    def __init__(self, a=0, b=0, c=0):
        self.a, self.b, self.c = a, b, c
        self.ptr = 0
        self.out = []

    def cmb(self, lit):
        if 0 <= lit <= 3:
            return lit
        else:
            return {4: self.a, 5: self.b, 6: self.c}[lit]

    def cycle(self, ins, lit):
        match ins:
            case 0:
                self.a = self.a // 2 ** self.cmb(lit)
            case 1:
                self.b ^= lit
            case 2:
                self.b = self.cmb(lit) % 8
            case 3:
                if self.a:
                    self.ptr = lit
                    self.ptr -= 2  # Do not increment if we jump
            case 4:
                self.b ^= self.c
            case 5:
                self.out.append(self.cmb(lit) % 8)
            case 6:
                self.b = self.a // 2 ** self.cmb(lit)
            case 7:
                self.c = self.a // 2 ** self.cmb(lit)

        self.ptr += 2

    def run(self, program):
        while self.ptr < len(program) - 1:
            self.cycle(program[self.ptr], program[self.ptr + 1])
        return self.out

    def output(self):
        return ','.join((str(s) for s in self.out))


@puzzle.solution_a
def solve_p1(data):
    vm, program = parse(data)
    vm.run(program)
    return vm.output()


@puzzle.solution_b
def solve_p2(data):
    """
    We have observed:
    - Output length goes up at 2^(3*i)
    - Each digit of the output follows the same cycle - ex. the last digit will always go 0,1,2,3,4,4,5,0
                and the 2nd last will always follow a 64-step pattern as well
    """

    base_vm, program = parse(data)
    b, c = base_vm.b, base_vm.c

    def result(targets):
        start = 0
        for x, t in enumerate(targets):
            start += t * 2 ** (3 * x)
        return start

    def check(targets):
        a = result([0] + targets)

        for j in range(0, 8):
            vm = VM(a + j, b, c)
            vm.run(program)
            if vm.out == program[-len(targets)-1:]:
                if len(vm.out) == len(program):
                    yield [j] + targets
                    return

                for new_targets in check([j] + targets):
                    yield new_targets

    for r in check([]):
        return result(r)

# puzzle.check_examples()
puzzle.check_solutions()
