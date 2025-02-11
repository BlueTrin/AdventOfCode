from aoc_lube import fetch

s = fetch(2021, 13)

print(s)

pts_s, fold_s = s.split('\n\n')

m = set()

for r in pts_s.splitlines():
    x, y = r.split(',')
    m.add((int(x), int(y)))


def do_fold(m, axis, pos):
    res = set()
    for x, y in m:
        if axis == 'x':
            if x <= pos:
                res.add((x, y))
            else:
                res.add((2 * pos - x, y))
        elif axis == 'y':
            if y <= pos:
                res.add((x, y))
            else:
                res.add((x, 2 * pos - y))
        else:
            raise ValueError(f"Invalid axis {axis}")
    return res

for i, r in enumerate(fold_s.splitlines()):
    d, pos = r.replace('fold along ', '').split('=')
    pos = int(pos)
    m = do_fold(m, d, pos)
    if i == 0:
        print(f"Part1: {len(m)}")

maxx = max(x for x, y in m)
maxy = max(y for x, y in m)

for y in range(maxy+1):
    for x in range(maxx+1):
        print('#' if (x, y) in m else ' ', end='')
    print()