from aoc_lube import fetch
import re
from utils.utils import Point
from collections import deque

import os

try:
    os.mkdir("d17_mazes")
except FileExistsError:
    pass

s = fetch(2018, 17)
# s = '''x=495, y=2..7
# y=7, x=495..501
# x=501, y=3..7
# x=498, y=2..4
# x=506, y=1..2
# x=498, y=10..13
# x=504, y=10..13
# y=13, x=498..504'''
# print(s)

clay = set()
for r in s.splitlines():
    m = re.match(r'(.)=(\d+), (.)=(\d+)\.\.(\d+)', r)
    for i in range(int(m[4]), int(m[5])+1):
        if m[1] == 'x':
            clay.add(Point(int(m[2]), i))
        elif m[1] == 'y':
            clay.add(Point(i, int(m[2])))
        else:
            raise RuntimeError("Invalid input")

water = set()

def fill_horizontally(pt, clay):
    new_sources = []
    new_water = {pt}
    for dir in [Point(1, 0), Point(-1, 0)]:
        curr = pt
        while curr + dir not in clay:
            curr += dir
            new_water.add(curr)
            if curr + Point(0, 1) not in clay:
                new_sources.append(curr)
                break
    return new_sources, new_water

def print_maze(clay, water, legend=None, file=None):
    if legend is None:
        legend = {}

    min_x = min(pt.x for pt in clay | water) -1
    max_x = max(pt.x for pt in clay | water) + 1
    min_y = 0
    max_y = max(pt.y for pt in clay | water)
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if Point(x, y) in legend:
                print(legend[Point(x, y)], end="", file=file)
            elif Point(x, y) == Point(500, 0):
                print("+", end="", file=file)
            elif Point(x, y) in water:
                if Point(x, y) in clay:
                    print("≡", end="", file=file)
                else:
                    print("~", end="", file=file)
            elif Point(x, y) in clay:
                print("#", end="", file=file)
            else:
                print(" ", end="", file=file)
        print("", file=file)

min_y = min(pt.y for pt in clay | water)
max_y = max(pt.y for pt in clay | water)

debug = False

iteration = 0
old_water_len = len(water)
while len(water) > old_water_len or not water:
    old_water_len = len(water)
    sources = deque([Point(500, 1)])
    past_sources = set()
    isource = 0
    while sources:
        source = sources.popleft()
        past_sources.add(source)
        print(f"processing {source}")
        water.add(source)
        # go vertically
        curr = source
        while (curr + Point(0, 1)) not in clay:
            curr += Point(0, 1)
            water.add(curr)
            if curr.y >= max_y:
                break

        if curr.y >= max_y:
            continue
        # fill horizontally
        new_sources = None
        while not new_sources:
            new_sources, new_water = fill_horizontally(curr, clay)
            water |= new_water
            if new_sources:
                sources.extend([x for x in new_sources if x not in past_sources and x not in sources])
                break
            else:
                clay |= new_water
                # go back up
                curr += Point(0, -1)

        if debug:
            print_maze(clay, water, legend={source:'S'}, file=open(f"d17_mazes/maze_{iteration:03}_{isource:03}.txt", "w"))
        isource += 1

    if debug:
        print_maze(clay, water, file=open(f"d17_mazes/maze_{iteration:03}.txt", "w"))
    iteration += 1

print_maze(clay, water, file=open("d17_mazes/maze.txt", "w"))
print(len([pt for pt in water if min_y <= pt.y <= max_y]))
# 38415 too high

print(len([pt for pt in water if min_y <= pt.y <= max_y and pt in clay]))
