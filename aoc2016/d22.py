from aoc_lube import fetch
from itertools import permutations
from utils2018.utils import Point
import re
from heapq import heappop, heappush


s = fetch(2016, 22)

nodes = {}
for r in s.splitlines()[2:]:
    if r is None:
        continue

    n, sz, us, av, usp = r.split()
    m = re.match(r'/dev/grid/node-x(\d+)-y(\d+)', n)
    if m is None:
        raise RuntimeError("Invalid input")

    nodes[Point(int(m.groups()[0]), int(m.groups()[1]))] = {'size': int(sz[:-1]), 'used': int(us[:-1]), 'avail': int(av[:-1]), 'usep': int(usp[:-1])}

avail = set()
total = 0
for c1, c2 in permutations(nodes, 2):
    if 0 < nodes[c1]['used'] <= nodes[c2]['avail']:
        total += 1
        avail.add(c1)

assert total == 901
print("Part1:", total)


# Part 2

start = Point(0, 0)
max_x = max(pt.x for pt in nodes)
max_y = max(pt.y for pt in nodes)
for pt in nodes:
    if pt.y == 0 and pt.x > start.x:
        start = pt

for y in range(max_y+1):
    for x in range(max_x+1):
        if Point(x, y) == start:
            print("S", end="")
        elif (x,y) == (0,0):
            print("G", end="")
        elif nodes[Point(x, y)]["used"] == 0:
            print("_", end="")
            empty = Point(x, y)
        elif Point(x, y) in avail:
            print(".", end="")
        else:
            print("#", end="")
    print("")


print(f"Empty: {empty} {nodes[empty]}")

# 230 too low
# 10 + 22 + 23 + 5 x 35 + 8
# just move the cursor on the map below
#
# G...................................S 23  (14 to 37)
# ..................................... + 5 x 35
# ..................................... move up 8
# .....................................
# .....................................
# .....................................
# .....................................
# ..............#######################
# ..................................... 10 + 22
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# ..................................._.
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
# .....................................
#
# 10 + 22 + 23 + 5 x 35
#
#
# 19, 36
# 9, 36
# 9, 14
