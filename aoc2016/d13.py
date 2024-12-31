from aoc_lube import fetch
from functools import cache
from utils.utils import Point

s = fetch(2016, 13)

fav = int(s)

@cache
def is_wall(x, y):
    return bin(x*x + 3*x + 2*x*y + y + y*y + fav).count('1') % 2

fill = {0: {Point(1,1)}}
seen = {Point(1,1)}
curr = 0
while True:
    curr += 1
    fill[curr] = set()
    for pt in fill[curr-1]:
        for d in [Point(0,1), Point(1,0), Point(0,-1), Point(-1,0)]:
            new_pt = pt + d
            if new_pt == Point(31,39):
                print("Part 1:", curr)
                raise SystemExit
            if new_pt in seen:
                continue
            if new_pt.x < 0 or new_pt.y < 0:
                continue
            if is_wall(new_pt.x, new_pt.y):
                continue
            fill[curr].add(new_pt)
            seen.add(new_pt)

    if curr == 50:
        print("Part 2:", len(seen))
    if len(fill[curr]) == 0:
        raise RuntimeError("No more moves")
