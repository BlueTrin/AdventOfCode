from aoc_lube import fetch
from intcode import Intcode
from collections import defaultdict

s = fetch(2019, 13)

p = list(map(int, s.strip().split(',')))

c = Intcode(p)
c.run()

m = defaultdict(set)

coords = [(c.output.popleft(), c.output.popleft(), c.output.popleft()) for i in range(0, len(c.output), 3)]
print(coords)

for x, y, t in coords:
    m[t].add((x, y))

print("part1: ", len(m[2]))

c = Intcode(p)
c.p[0] = 2
while not c.halted:
    c.run()
    m = defaultdict(set)
    coords = [(c.output.popleft(), c.output.popleft(), c.output.popleft()) for i in range(0, len(c.output), 3)]
    for x, y, t in coords:
        if x == -1 and y == 0:
            print(f"score: {t}")
        else:
            m[t].add((x, y))
    ball = next(iter(m[4]))
    if 3 in m:
        paddle = next(iter(m[3]))
    walls = m[1]
    bdir = None

    if bdir is None:
        c.add_input((ball[0] - paddle[0]) // abs(ball[0] - paddle[0]) if  ball[0] != paddle[0] else 0)
    else:
        c.add_input(bdir)
#    print(f"ball: {ball}, paddle: {paddle}, walls: {walls}")

pass