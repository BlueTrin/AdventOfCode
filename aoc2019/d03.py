from aoc_lube import fetch
from utils.utils import Point, FOURDIRS

s = fetch(2019, 3)
# s = '''R8,U5,L5,D3
# U7,R6,D4,L4'''
def manhattan(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))

LET2DIR = {'U': Point(0, -1), 'D': Point(0, 1), 'L': Point(-1, 0), 'R': Point(1, 0)}

wires = []
for r in s.splitlines():
    curr = Point(0, 0)
    wire = r.split(',')
    wire_map = []
    for d in wire:
        direction = LET2DIR[d[0]]
        distance = int(d[1:])
        for _ in range(distance):
            curr += direction
            wire_map.append(curr)
    wires.append(wire_map)

print("Part1: ", min([manhattan(x, Point(0, 0)) for x in set.intersection(set(wires[0]), set(wires[1]))]))

print("Part2: ", min([2+wires[0].index(x)+wires[1].index(x) for x in set.intersection(set(wires[0]), set(wires[1]))]))

pass

