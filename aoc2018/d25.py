import itertools

from aoc_lube import fetch
from collections import deque

s = fetch(2018, 25)

def manhattan(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))

points = [tuple(map(int, i.split(','))) for i in s.splitlines()]

links = {}
for pt1, pt2 in itertools.combinations(points, 2):
    if manhattan(pt1, pt2) <= 3:
        links.setdefault(pt1, []).append(pt2)
        links.setdefault(pt2, []).append(pt1)

single_pts = [pt for pt in points if pt not in links]

constellation_lst = []
while links:
    q = deque([links.popitem()])
    constellation = set()
    while q:
        pt, neighbors = q.popleft()
        constellation.add(pt)
        for neighbor in neighbors:
            if neighbor in links:
                q.append((neighbor, links.pop(neighbor)))
    constellation_lst.append(constellation)

print(len(constellation_lst) +len(single_pts))
# 127 too low
pass
# 597 too high