import itertools

from aoc_lube import fetch
import re
from collections import namedtuple


class Point(namedtuple('Point',['x', 'y'])):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y )

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

s = fetch(2018, 10)

pt_lst = []
for r in s.splitlines():
    if not r:
        continue
    _, x, y, _, vx, vy, _ = re.split(r'[ <>, ]+', r)
    x, y, vx, vy = int(x), int(y), int(vx), int(vy)
    pt_lst.append((Point(x, y), Point(vx, vy)))

def get_pos(pt_lst, t):
    new_lst = []
    for pt, vel in pt_lst:
        new_lst.append(pt + vel*t)

    return new_lst

def entropy(pt_lst):
    total = 0
    for pt1, pt2 in itertools.combinations(pt_lst, 2):
        if abs(pt1.x - pt2.x) <= 1 and abs(pt1.y - pt2.y) <= 1:
            total += 1
    return total

def print_lst(new_lst, t=10577):
    new_lst = get_pos(new_lst, t)
    min_x = min(pt.x for pt in new_lst)
    min_y = min(pt.y for pt in new_lst)
    max_x = max(pt.x for pt in new_lst)
    max_y = max(pt.y for pt in new_lst)
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x + 1):

            if Point(x, y) in new_lst:
                print("#", end="")
            else:
                print(" ", end="")
        print("")

print_lst(pt_lst)

while True:
    for t in range(100000):
        new_lst =get_pos(pt_lst, t)
        min_x = min(pt.x for pt in new_lst)
        min_y = min(pt.y for pt in new_lst)
        max_x = max(pt.x for pt in new_lst)
        max_y = max(pt.y for pt in new_lst)
        print(t, max_x - min_x, max_y - min_y)


