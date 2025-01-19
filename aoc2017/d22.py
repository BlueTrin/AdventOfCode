from aoc_lube import fetch
from utils.utils import Point

s = fetch(2017, 22)

m = {}
for iy, r in enumerate(s.splitlines()):
    for ix, c in enumerate(r):
        m[Point(ix, iy)] = c

pos = Point(len(r) // 2, len(s.splitlines()) // 2)
d = Point(0, -1)

infections = 0
steps = 0
while steps < 10000:
    if m.get(pos, '.')== '#':
        d = d.rotate(90)
        m[pos] = '.'
    elif m.get(pos, '.') == '.':
        d = d.rotate(-90)
        m[pos] = '#'
        infections += 1
    else:
        raise NotImplementedError()
    pos += d
    steps += 1

print(f"Part1: {infections}")

def p2(s, max_steps):
    m = {}
    for iy, r in enumerate(s.splitlines()):
        for ix, c in enumerate(r):
            m[Point(ix, iy)] = c

    pos = Point(len(r) // 2, len(s.splitlines()) // 2)
    d = Point(0, -1)

    infections = 0
    steps = 0
    while steps < max_steps:
        if m.get(pos, '.')== '#':
            # Infected nodes become flagged.
            m[pos] = 'F'
            # If it is infected, it turns right.
            d = d.rotate(90)
        elif m.get(pos, '.') == '.':
            # Clean nodes become weakened.
            m[pos] = 'W'
            # If it is clean, it turns left.
            d = d.rotate(-90)
        elif m.get(pos, '.') == 'W':
            # Weakened nodes become infected.
            m[pos] = '#'
            infections += 1
            # If it is weakened, it does not turn, and will continue moving in the same direction.
        elif m.get(pos, '.') == 'F':
            # Flagged nodes become clean.
            m[pos] = '.'
            # If it is flagged, it reverses direction, and will go back the way it came.
            d = d.rotate(180)
        else:
            raise NotImplementedError()
        pos += d
        steps += 1

    return infections, m

infected, m = p2('''..#
#..
...''', 100)
assert infected == 26

infected, m = p2('''..#
#..
...''', 10000000)
assert infected == 2511944

print("doing part2")
infections, m = p2(s, 10000000)

print(f"Part2: {infections}")
