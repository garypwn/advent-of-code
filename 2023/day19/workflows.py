import itertools
import re

_workflow_pattern = re.compile(r"^(\w+){(\S+)}$")
_condition_pattern = re.compile(r"(\w+)(?:([<>])(\d+):(\w+))?(?=$|,)")
_attribute_pattern = re.compile(r"([xmas])=(\d+)")


def _parse_attr(s):
    d = {}
    for m in _attribute_pattern.finditer(s):
        label, value = m.groups()
        d[label] = int(value)

    return d


def _parse_condition(s):
    for m in _condition_pattern.finditer(s):
        if not m.group(2):
            yield m.group(1), (None, None, None)
        else:
            arg1, fun, arg2, target = m.groups()
            yield target, (arg1, int(arg2), fun == '>')


def _eval(part, cond):
    arg1, arg2, gt = cond
    if arg1 is None:
        return True

    if gt:
        return part[arg1] > arg2
    else:
        return part[arg1] < arg2


def _boundary(cond):
    # Exclusive boundary
    attribute, arg2, gt = cond
    if attribute is None:
        return None
    if gt:
        return arg2 + 1
    else:
        return arg2


def _parse_workflow(s):
    m = _workflow_pattern.match(s)
    if not m:
        return None

    label, wf = m.groups()
    return label, list(_parse_condition(wf))


def parse(lines):
    it = iter(lines)

    workflows = {}
    for line in it:
        if line == '\n':
            break

        label, conditions = _parse_workflow(line)
        workflows[label] = conditions

    parts = [_parse_attr(line) for line in it]

    return parts, workflows


class Workflows:

    def __init__(self, workflows):
        self.workflows = workflows

    def accepted(self, part):
        curr = 'in'
        while True:
            if curr == 'R':
                return False
            elif curr == 'A':
                return True

            for target, condition in self.workflows[curr]:
                if _eval(part, condition):
                    curr = target
                    break


def solve(lines):
    parts, workflows = parse(lines)
    workflows = Workflows(workflows)

    accepted = [sum(part.values()) for part in parts if workflows.accepted(part)]
    return sum(accepted)


def solve_p2(lines, min_val=1, max_val=4000):
    parts, workflows = parse(lines)
    workflows = Workflows(workflows)

    b = ((c[0], _boundary(c)) for wf in workflows.workflows.values() for _, c in wf if c[0] is not None)

    bounds = {s: [min_val] for s in 'xmas'}
    for attr, bound in b:
        bounds[attr].append(bound)

    for s in 'xmas':
        bounds[s].sort()
        bounds[s].append(max_val + 1)

    accepted = 0

    for x, m, a, s in itertools.product(*(itertools.pairwise(bounds[a]) for a in 'xmas')):
        part = {'x': x[1] - 1, 'm': m[1] - 1, 'a': a[1] - 1, 's': s[1] - 1}
        power = 1
        for n1, n2 in (x, m, a, s):
            power *= n2 - n1

        if workflows.accepted(part):
            accepted += power

    return accepted
