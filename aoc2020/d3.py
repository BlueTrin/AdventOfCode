from aoc_lube import fetch
from utils.utils import Point

s = fetch(2020, 3)

rows = s.splitlines()

pos = Point(0, 0)
d = Point(3, 1)

trees = 0
while pos.y < len(rows):
    if rows[pos.y][pos.x % len(rows[pos.y])] == '#':
        trees += 1
    pos += d

print(f"Part1: {trees}")
assert trees == 254

p2 = 1
for d in [Point(1, 1), Point(3, 1), Point(5, 1), Point(7, 1), Point(1, 2)]:
    pos = Point(0, 0)

    trees = 0
    while pos.y < len(rows):
        if rows[pos.y][pos.x % len(rows[pos.y])] == '#':
            trees += 1
        pos += d

    p2 *= trees

print(f"Part2: {p2}")