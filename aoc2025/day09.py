from aoc_lube import fetch
import math
import logging
from typing import Tuple, Set, List, Dict
from functools import cache
import numpy as np
from utils.utils import (Point, parse_point, EIGHTDIRS, FOURDIRS)
import copy
from scipy.ndimage import convolve
from collections import defaultdict
import networkx as nx

logging.basicConfig(level=logging.DEBUG)
s = fetch(2025, 9)
#
# s = '''7,1
# 11,1
# 11,7
# 9,7
# 9,5
# 2,5
# 2,3
# 7,3'''

# # add a networkx graph
# G = nx.Graph()
#
# # directional graph
# G = nx.DiGraph()
#
# # add edge with weight
# G.add_edge(1, 2, weight=3)
part1 = None
part2 = None

pts = []
for coord_str in s.split('\n'):
    x, y = coord_str.split(',')
    pts.append((int(x), int(y)))

part1 = 0
for i, (x, y) in enumerate(pts):
    for j in range(i+1, len(pts)):
        x2, y2 = pts[j]
        area = (abs(x2 - x)+1) * (abs(y2 - y)+1)

        part1 = max(part1, area)

print(f"part 1: {part1}")


min_x = min([x for x, y in pts])
max_x = max([x for x, y in pts])
min_y = min([y for x, y in pts])
max_y = max([y for x, y in pts])
m = {}
for pt1, pt2 in zip(pts, pts[1:] + [pts[0]]):

    for x in range(min(pt1[0], pt2[0]), max(pt1[0], pt2[0])+1):
        for y in range(min(pt1[1], pt2[1]), max(pt1[1], pt2[1])+1):
            m[(x, y)] = 'X'
    m[pt1] = '#'
    m[pt2] = '#'

def neighbours(pt: Tuple[int, int], dirs = EIGHTDIRS):
    x, y = pt
    for dx, dy in dirs:
        yield (x+dx, y+dy)

def is_neighbour(pt1: Tuple[int, int], grid: Set[Tuple[int, int]], dirs = EIGHTDIRS):
    for npt in neighbours(pt1, dirs=dirs):
        if npt in grid:
            return True
    return False

def outside_perimeter(
        walls: set[Tuple[int, int]],
):
    from collections import deque
    perimeter = set()

    min_x = min(pt[0] for pt in walls)
    max_x = max(pt[0] for pt in walls)
    min_y = min(pt[1] for pt in walls)
    max_y = max(pt[1] for pt in walls)

    for x in range(min_x-1, max_x+2):
        if (x+1, min_y) in walls:
            start_pt = (x, min_y-1)

    d = deque([start_pt])
    perimeter.add(start_pt)
    while d:
        pt = d.pop()
        for npt in neighbours(pt, dirs=FOURDIRS):
            if npt in walls:
                continue
            if npt in perimeter:
                continue
            if not (min_x-1 <= npt[0] <= max_x+1 and min_y-1 <= npt[1] <= max_y+1):
                continue
            if is_neighbour(npt, walls, dirs=EIGHTDIRS):
                perimeter.add(npt)
                d.append(npt)

    return perimeter

logging.info(f"Flood filling from outside")
perimeter = outside_perimeter(
    walls=set(m.keys()),
)
logging.info(f"  -> DONE")

if max_y < 50:
    for pt in perimeter:
        m[pt] = '.'
    for x in range(min_x-1 , max_x +2):
        for y in range(min_y-1, max_y +2):
            print(m.get((x, y), ' '), end='')
        print('')


logging.info(f"Finding part2 largest area")
part2 = 0
for i, (x, y) in enumerate(pts):
    logging.info(f" Checking pt {i+1}/{len(pts)}: {pts[i]}")

    # let's determine min_ix, max_ix, min_iy, max_iy for this point
    for min_ix in range(x, min_x, -1):
        if (min_ix-1, y) in perimeter:
            break
    for max_ix in range(x, max_x+1):
        if (max_ix+1, y) in perimeter:
            break
    for min_iy in range(y, min_y, -1):
        if (x, min_iy-1) in perimeter:
            break
    for max_iy in range(y, max_y+1):
        if (x, max_iy+1) in perimeter:
            break
    for j in range(i+1, len(pts)):
        x2, y2 = pts[j]

        if not (min_ix <= x2 <= max_ix):
            continue
        if not (min_iy <= y2 <= max_iy):
            continue

        area = (abs(x2 - x)+1) * (abs(y2 - y)+1)
        if area <= part2:
            continue
        # check if we found in the outside perimeter
        found_dot = False
        for xx in range(min(x, x2), max(x, x2)+1):
            if found_dot:
                break
            if (xx, y) in perimeter:
                found_dot = True
            if (xx, y2) in perimeter:
                found_dot = True
        for yy in range(min(y, y2), max(y, y2)+1):
            if found_dot:
                break
            if (x, yy) in perimeter:
                found_dot = True
            if (x2, yy) in perimeter:
                found_dot = True
        if not found_dot:
            part2 = max(part2, area)
            logging.info(f"  New largest area {part2} for pts {pts[i]} and {pts[j]}")
print(f"part 2: {part2}")
