from aoc_lube import fetch
from utils.utils import Point as Pt

s = fetch(2020, 12)

print(s)

def execute(s, p2=False, verbose=False):
    pos = Pt(0, 0)
    if p2:
        d = Pt(10, -1)
    else:
        d = Pt(1, 0)

    DIR2PT = {
        'N': Pt(0, -1),
        'E': Pt(1, 0),
        'S': Pt(0, 1),
        'W': Pt(-1, 0),
    }

    for r in s.splitlines():
        a = r[0]
        n = int(r[1:])
        if a in DIR2PT:
            if p2:
                d += DIR2PT[a]*n
            else:
                pos += DIR2PT[a]*n
        elif a == 'F':
            pos += d*n
        elif a == 'L':
            d = d.rotate(-n)
        elif a == 'R':
            d = d.rotate(n)

        if verbose:
            print(f"{r} -> {pos}")
    return pos

pos = execute('''F10
N3
F7
R90
F11''', verbose=True)
assert pos.manhattan(Pt(0, 0)) == 25

pos = execute(s)
print(f"Part1: {abs(pos.x) + abs(pos.y)}")

pos = execute(s, p2=True)
print(f"Part2: {abs(pos.x) + abs(pos.y)}")
