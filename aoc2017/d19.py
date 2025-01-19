from aoc_lube import fetch
from utils.utils import Point

s = fetch(2017, 19)

xs = s.splitlines()[0].index('|')

m = {}
for iy, r in enumerate(s.splitlines()):
    for ix, c in enumerate(r):
        if c == ' ':
            continue
        m[Point(ix, iy)] = c

p = Point(xs, 0)
d = Point(0, 1)

d2c = {
    Point(0, 1): '|',
    Point(0, -1): '|',
    Point(1, 0): '-',
    Point(-1, 0): '-'
}

debug = False
steps = 0
letters = []
while True:
    p += d
    steps += 1
    if debug:
        print(p, d, m.get(p))
    if p not in m:
        break
    if m[p] == '+':
        if debug:
            for y in range(p.y - 3, p.y + 4):
                for x in range(p.x - 3, p.x + 4):
                    print(m.get(Point(x, y), " "), end="")
                print()

        for dd in [d, d.rotate(90), d.rotate(-90)]:
            straight = p + dd
            straight_letters = []
            while straight in m and m[straight] not in ['+', d2c[dd]]:
                if 'A' <= m[straight] <= 'Z':
                    straight_letters += m[straight]
                straight += dd
            if m.get(straight) in ['+', d2c[dd]]:
                # we can go straight
                steps += p.manhattan(straight)
                p = straight
                d = dd
                letters.extend(straight_letters)
                break
    elif 'A' <= m[p] <= 'Z':
        letters.append(m[p])
    elif m[p] == d2c[d]:
        continue
print(f"Part1: {''.join(letters)}")
print(f"Part2: {steps}")