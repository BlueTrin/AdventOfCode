from aoc_lube import fetch

from utils.utils import Point

all_pt = []
for r in fetch(2018, 6).splitlines():
    all_pt.append(Point(*map(int, r.split(", "))))

print(all_pt)

def manhattan(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

x_min = min(pt.x for pt in all_pt)
x_max = max(pt.x for pt in all_pt)
y_min = min(pt.y for pt in all_pt)
y_max = max(pt.y for pt in all_pt)

areas  = [0] * len(all_pt)
for x in range(x_min-10, x_max+10):
    for y in range(y_min-10, y_max+10):
        pt = Point(x, y)
        min_dist = 999999999
        min_pt = []
        for ip, p in enumerate(all_pt):
            if manhattan(pt, p) < min_dist:
                min_dist = manhattan(pt, p)
                min_pt = [p]
            elif manhattan(pt, p) == min_dist:
                min_pt.append(p)

        if len(min_pt) == 1:
            areas[ip] += 1
pass