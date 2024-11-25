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

    def accepted_range(self, p_range, curr):
        if curr == 'R':
            return 0
        if curr == 'A':
            prod = 1
            for c in 'xmas':
                prod *= p_range[1][c] - p_range[0][c]

            return prod

        accepted = 0
        remainder = p_range

        for target, cond in self.workflows[curr]:
            if remainder is None:
                break

            if cond[0] is not None:
                remainder, passed = _eval_range(remainder, cond)
            else:
                remainder, passed = None, remainder
            if passed is not None:
                accepted += self.accepted_range(passed, target)

        return accepted


def solve(lines):
    parts, workflows = parse(lines)
    workflows = Workflows(workflows)

    accepted = [sum(part.values()) for part in parts if workflows.accepted(part)]
    return sum(accepted)


def _eval_range(p_range: tuple[dict[str: int]], cond):
    # Splits a range into (false, true) sub ranges

    attr, value, gt = cond
    bound = _boundary(cond)

    if p_range[0][attr] <= bound < p_range[1][attr]:
        # Splitting range
        below = (p_range[0].copy(), {t: bound if t == attr else v for t, v in p_range[1].items()})
        above = ({t: bound if t == attr else v for t, v in p_range[0].items()}, p_range[1].copy())

    else:
        if bound > p_range[0][attr]:
            below, above = p_range, None
        else:
            below, above = None, p_range

    if gt:
        return below, above
    else:
        return above, below


def solve_p2(lines, min_val=1, max_val=4000):
    parts, workflows = parse(lines)
    workflows = Workflows(workflows)

    p_range = ({c: min_val for c in 'xmas'}, {c: max_val + 1 for c in 'xmas'})
    return workflows.accepted_range(p_range, 'in')
