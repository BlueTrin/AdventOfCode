from aoc_lube import fetch
from utils.utils import Point3D
import re
import itertools
from pprint import pp
import math


s = fetch(2019, 12)
max_steps = 1000

# s = '''<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>'''
# max_steps = 10

def init_moons(s):
    moons = []
    for r in s.splitlines():
        m = re.split(r'[<,>=]', r)
        x, y, z = map(int, (m[2], m[4], m[6]))
        moons.append([Point3D(x, y, z), Point3D(0, 0, 0)])
    return moons

moons = init_moons(s)
debug = True
for steps in range(max_steps):
    for m1, m2 in itertools.combinations(range(len(moons)), 2):
        g1 = Point3D(*[int((x2-x1)/abs(x2-x1)) if x2 != x1 else 0 for x1, x2 in zip(moons[m1][0], moons[m2][0])])
        moons[m1][1] += g1
        moons[m2][1] -= g1

    for m in moons:
        m[0] += m[1]

    if debug:
        pp(moons)

# The total energy for a single moon is its potential energy multiplied by its kinetic energy. A moon's potential energy
# is the sum of the absolute values of its x, y, and z position coordinates. A moon's kinetic energy is the sum of the
# absolute values of its velocity coordinates.
print(sum(sum(abs(x) for x in m[0]) * sum(abs(x) for x in m[1]) for m in moons))


xcycle, ycycle, zcycle = None, None, None
istep = 0
xseen, yseen, zseen = {}, {}, {}

moons = init_moons(s)
while xcycle is None or ycycle is None or zcycle is None:
    istep += 1
    for m1, m2 in itertools.combinations(range(len(moons)), 2):
        g1 = Point3D(*[int((x2-x1)/abs(x2-x1)) if x2 != x1 else 0 for x1, x2 in zip(moons[m1][0], moons[m2][0])])
        moons[m1][1] += g1
        moons[m2][1] -= g1

    for m in moons:
        m[0] += m[1]

    if not xcycle:
        xcoords = tuple((m[0].x, m[1].x) for m in moons)
        if xcoords in xseen:
            xcycle = istep - xseen[xcoords]
        else:
            xseen[xcoords] = istep
    if not ycycle:
        ycoords = tuple((m[0].y, m[1].y) for m in moons)
        if ycoords in yseen:
            ycycle = istep - yseen[ycoords]
        else:
            yseen[ycoords] = istep
    if not zcycle:
        zcoords = tuple((m[0].z, m[1].z) for m in moons)
        if zcoords in zseen:
            zcycle = istep - zseen[zcoords]
        else:
            zseen[zcoords] = istep

# intuition: x, y, z are independent, so the cycle is the least common multiple of the cycles of x, y, z
print(math.lcm(xcycle, ycycle, zcycle))