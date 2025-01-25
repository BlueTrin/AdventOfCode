from aoc_lube import fetch
from utils.utils import Point3D as P3D
from collections import defaultdict
import itertools

s = fetch(2020, 17)

# s = '''.#.
# ..#
# ###'''
print(s)




def adjacent(p, diagonals=True):
    if diagonals:
        return tuple(tuple(p[i] + d[i] for i in range(len(p))) for d in itertools.product((-1, 0, 1), repeat=len(p)) if any(d))
    else:
        # do something more efficient ...
        return tuple(tuple(p[i] + d[i] for i in range(len(p))) for d in itertools.product((-1, 0, 1), repeat=len(p)) if any(d) and sum(d) == 1)

def next_state(m, debug=False):
    n = defaultdict(int)
    for p, status in m.items():
        if status == 0:
            continue
        for dp in adjacent(p, diagonals=True):
            n[dp] += 1
    for p in set(n.keys()) | set(m.keys()):
        # f a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active.
        # Otherwise, the cube becomes inactive.
        if m[p]:
            if n[p] == 3 or n[p] == 2:
                m[p] = 1
            else:
                m[p] = 0
        elif n[p] == 3:
            # If a cube is inactive but exactly 3 of its neighbors are active,
            # the cube becomes active. Otherwise, the cube remains inactive.
            m[p] = 1
    return m


def solve(s, part2=False):
    m = defaultdict(int)
    for iy, r in enumerate(s.splitlines()):
        for ix, c in enumerate(r):
            if c == '#':
                if part2:
                    m[(ix, iy, 0, 0)] = 1
                else:
                    m[(ix, iy, 0)] = 1


    for i in range(6):
        print(f"Cycle {i}")
        m = next_state(m)
        print(f"Active: {sum(m.values())}")

    return m
#
# m = solve(s)
# print(f"Part1: {sum(m.values())}")
# # 370 too high ?

m = solve(s, part2=True)
print(f"Part2: {sum(m.values())}")
