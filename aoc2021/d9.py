from aoc_lube import fetch
import numpy as np
from itertools import product
from collections import deque, defaultdict
from operator import mul
from functools import reduce

s = fetch(2021, 9)
# s = '''2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678'''
m = {}

FOURDIRS = [(dx, dy) for dx, dy in product([-1, 0, 1], repeat=2) if (dx == 0) ^ (dy == 0)]

for iy, row in enumerate(s.splitlines()):
    for ix, c in enumerate(row):
        m[ix, iy] = int(c)

# What is the sum of the risk levels of all low points on your heightmap?
p1 = 0
low_points = []
for c, height, in m.items():
    if all(m.get((c[0]+dx, c[1]+dy), 10)  > height for dx, dy in product([-1, 0, 1], repeat=2) if (dx==0) ^ (dy==0)):
        # The risk level of a low point is 1 plus its height
        p1 += height+1
        low_points.append(c)

print(f"Part1: {p1}")

def neighbours(c):
    for dx, dy in FOURDIRS:
        yield c[0]+dx, c[1]+dy


def bassin_size(c, m):
    bass_by_height = defaultdict(set)
    height = m[c]
    bass_by_height[height] = {c}

    invalid_height = False
    while not invalid_height:
        height += 1

        bass_by_height[height] = bass_by_height[height-1].copy()
        d = deque(bass_by_height[height-1])
        while d:
            x = d.popleft()
            for n in neighbours(x):
                if n not in m or n in bass_by_height[height]:
                    continue
                if m[n] == height:
                    bass_by_height[height].add(n)
                    d.append(n)

        for x in bass_by_height[height]:
            for n in neighbours(x):
                if n not in m or n in bass_by_height[height]:
                    continue
                if m[n] < height:
                    invalid_height = True
                    break
            else:
                continue
            break

    return len(bass_by_height[height-1])

bassins_sizes = []
for c in low_points:
    if c in m:
        bassins_sizes.append(bassin_size(c, m))

print(f"Part2: {reduce(mul, sorted(bassins_sizes, reverse=True)[:3], 1)}")
# 43680 too low