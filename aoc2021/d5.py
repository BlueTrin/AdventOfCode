from aoc_lube import fetch
import numpy as np
from collections import defaultdict
import logging

s = fetch(2021, 5)

# s = '''0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2'''
minx, maxx, miny, maxy = 99999999, -99999999, 99999999, -99999999

segments = []
for row in s.splitlines():
    left, right = row.split(' ->')
    l = np.array([int(x) for x in left.split(',')])
    r = np.array([int(x) for x in right.split(',')])
    segments.append((l, r))
    minx = min(minx, l[0])
    maxx = max(maxx, r[0])
    miny = min(miny, l[1])
    maxy = max(maxy, r[1])

sign = lambda x: int(x > 0) - int(x < 0)

grid = defaultdict(int)
grid2 = defaultdict(int)
for l, r in segments:
    d = np.array([sign(r[0] - l[0]), sign(r[1] - l[1])])
    p = l
    while np.any(p-d != r):
        grid2[tuple(p)] += 1
        if d[0] != 0 and d[1] != 0:
            # For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.
            p += d
            continue
        grid[tuple(p)] += 1
        p += d
    # print(f"l: {l}, r: {r}, grid: {grid}")
    pass

print(f"Part1: {sum([v > 1 for v in grid.values()])}")
# 5576
print(f"Part2: {sum([v > 1 for v in grid2.values()])}")
# 955571 too high