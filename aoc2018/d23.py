from aoc_lube import fetch
from utils.utils import Point3D
import re

s = fetch(2018, 23)

bots = []
for r in s.splitlines():
    if r is None:
        continue

    _, x, y, z, r = re.split(r'[a-z <>,=]+', r)
    x,y,z,r = int(x), int(y), int(z), int(r)
    bots.append((Point3D(x, y, z), r))

strongest = max(bots, key=lambda x: x[1])

def manhattan(pt1, pt2):
    return sum(abs(a-b) for a, b in zip(pt1, pt2))

total = 0
for b in bots:
    if manhattan(b[0], strongest[0]) <= strongest[1]:
        total += 1

print(total)


from z3 import *

x, y, z = Ints('x y z')

def z3abs(x):
    return If(x >= 0,x,-x)

o = Optimize()

in_rng = [Int(f'in_rng_{i}') for i in range(len(bots))]

for i in range(len(bots)):
    o.add(in_rng[i] == If(z3abs(x - bots[i][0].x) + z3abs(y - bots[i][0].y) + z3abs(z - bots[i][0].z) <= bots[i][1], 1, 0))

o.maximize(Sum(in_rng))
o.minimize(z3abs(x) + z3abs(y) + z3abs(z))
assert o.check() == sat
print(o.model()[x].as_long() + o.model()[y].as_long() + o.model()[z].as_long())



pass