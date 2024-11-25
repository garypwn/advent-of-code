from utils.aocd_solutions import Puzzle

puzzle = Puzzle(2022, 7)

def make_fs(data: str):
    root = dict()
    cd = root

    for entry in data.split("$ "):

        if entry == '':
            continue

        lines = entry.strip().split('\n')

        # ls
        if lines[0][0] == 'l':
            for line in lines[1:]:

                # Files
                if line[0].isdigit():
                    size, name = line.split(' ')
                    cd[name] = int(size)

                # Directories
                else:
                    s, name = line.split(' ')
                    assert s == 'dir'
                    cd[name] = {'..': cd}

        # cd
        else:
            cmd, tgt = lines[0].split(' ')
            assert cmd == 'cd'

            if tgt == '/':
                cd = root
            else:
                assert tgt in cd
                cd = cd[tgt]

    return root

def dir_size(directory: dict):
    if '.size' in directory:
        return directory['.size']

    size = 0
    for k, v in directory.items():
        if k[0] == '.':
            continue
        if isinstance(v, int):
            size += v
        else:
            size += dir_size(v)

    directory['.size'] = size
    return size

def directories(directory: dict):
    for k, v in directory.items():
        if k[0] == '.':
            continue
        if isinstance(v, dict):
            for d in directories(v):
                yield d

            yield v

@puzzle.solution_a
def solve_p1(data):
    root = make_fs(data)
    total = 0
    for d in directories(root):
        s = dir_size(d)
        if s <= 100000:
            total += s

    return total

@puzzle.solution_b
def solve_p2(data):
    root = make_fs(data)
    smallest_deletable = dir_size(root)
    req_space = 30000000 - 70000000 + dir_size(root)
    for d in directories(root):
        if dir_size(d) >= req_space:
            smallest_deletable = min(smallest_deletable, dir_size(d))

    return smallest_deletable

puzzle.check_examples()
puzzle.check_solutions()
