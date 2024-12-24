import operator
import re

from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2024, 24)


def parse(data):
    initial, gates = data.split('\n\n')

    pattern1 = re.compile(r"(.+): (\d)")

    def parse_initial(vals):
        for line in vals.split('\n'):
            s, x = pattern1.match(line).groups()
            yield s, bool(int(x))

    pattern2 = re.compile(r"(.+) (OR|AND|XOR) (.+) -> (.+)")

    def parse_gates(vals):
        for line in vals.split('\n'):
            op1, op, op2, res = pattern2.match(line).groups()
            yield op1, op2, op, res

    return parse_initial(initial), parse_gates(gates)


def get_output(name, gates, outputs):
    if name in outputs:
        return outputs[name]

    op1, op2, op = gates[name]
    match op:
        case 'AND':
            op = operator.and_
        case 'OR':
            op = operator.or_
        case 'XOR':
            op = operator.xor

    op1, op2 = (get_output(o, gates, outputs) for o in (op1, op2))
    result = op(op1, op2)
    outputs[name] = result
    return result


def combine_bits(bits):
    result = 0
    for b in bits:
        result <<= 1
        result ^= b
    return result


def find_half_adder(in1, in2, gates):
    out, outc = None, None

    for k, (op1, op2, op) in gates.items():
        if {op1, op2} == {in1, in2}:
            if op == 'XOR':
                out = k
            if op == 'AND':
                outc = k

    return out, outc


def find_full_adder(in1, in2, inc, gates):
    xor1, out = None, None
    and1, and2, outc = None, None, None  # Carry block

    for i in range(4):
        if all((out, outc, xor1, and1, and2)):
            break

        for k, (op1, op2, op) in gates.items():
            if {op1, op2} == {in1, in2}:
                if op == 'XOR':
                    xor1 = k
                if op == 'AND':
                    and2 = k


            elif xor1 and {op1, op2} == {inc, xor1}:
                if op == 'XOR':
                    out = k
                if op == 'AND':
                    and1 = k

            elif and1 and and2 and {op1, op2} == {and1, and2}:
                if op == 'OR':
                    outc = k

    return out, outc, xor1, and1, and2


@puzzle.solution_a
def solve_p1(data):
    initial, gates = parse(data)
    gates = {res: (op1, op2, op) for op1, op2, op, res in gates}
    outputs = {w: v for w, v in initial}

    z_count = max([int(z[1:]) for z in gates.keys() if z[0] == 'z'])
    return combine_bits((get_output(f"z{i:02}", gates, outputs) for i in reversed(range(z_count + 1))))


@puzzle.solution_b
def solve_p2(data):
    initial, gates = parse(data)
    gates = {res: (op1, op2, op) for op1, op2, op, res in gates}
    z_count = max([int(z[1:]) for z in gates.keys() if z[0] == 'z'])

    carry = None
    bad_wires = []
    fixed_wires = []
    i = 0
    while i < z_count - 1:
        x, y, z = (f"{s}{i:02}" for s in "xyz")
        if i == 0:
            result = find_half_adder(x, y, gates)
        else:
            result = find_full_adder(x, y, carry, gates)

        out, outc = result[:2]
        extras = result[2:]

        none_ct = 0
        if out is None:
            none_ct += 1
        elif out != z:
            bad_wires.append(out)

        for wire in extras + (outc,):
            if not wire:
                none_ct += 1
            elif wire[0] in 'xyz':
                bad_wires.append(wire)

        if none_ct == 3:
            bad_wires += [w for w in result if w is not None]

        if bad_wires:
            w1, w2 = bad_wires
            gates[w1], gates[w2] = gates[w2], gates[w1]
            fixed_wires += [w1, w2]
            bad_wires.clear()
        else:
            carry = outc
            i += 1

    fixed_wires.sort()
    return ','.join(fixed_wires)


puzzle.check_solutions()
