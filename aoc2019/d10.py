from aoc_lube import fetch
from utils.utils import Point
from collections import defaultdict
import math

s = fetch(2019, 10)
ast = set()
for iy, r in enumerate(s.splitlines()):
    for ix, c in enumerate(r):
        if c == '#':
            ast.add(Point(ix, iy))


max_count = 0
best_ast = None
for a1 in ast:
    count = 0
    vis_ang = set()
    for a2 in ast:
        if a1 == a2:
            continue
        ang = (a2.y - a1.y, a2.x - a1.x)


        ang =(ang[0]/math.gcd(ang[0], ang[1]), ang[1]/math.gcd(ang[0], ang[1]))
        vis_ang.add(ang)

    count += len(vis_ang)
    if count > max_count:
        max_count = count
        best_ast = a1

print(f"Part 1: {max_count} {best_ast}")
assert max_count == 260

angles = defaultdict(list)
for a in ast:
    if a == best_ast:
        continue
    # we start at 90 degrees and go clockwise, so we invert the y and x and flip the sign of y
    ang = Point(-a.y + best_ast.y, a.x - best_ast.x).angle()
    if ang < 0:
        ang += 360.0
    angles[ang].append(a)

for angle in sorted(angles.keys()):
    angles[angle].sort(key=lambda a: best_ast.manhattan(a))
#
vaporised = 0
for angle in sorted(angles.keys()):
    vaporised += 1
    if vaporised == 200:
        print(f"Part 2: {angles[angle][0].x*100 + angles[angle][0].y}")
        break

# 2300 too high

def angle(start, end):
    result = math.atan2(end[0] - start[0], start[1] - end[1]) * 180 / math.pi
    angle_pt = Point(-end.y + start.y, end.x - start.x).angle()
    assert result == angle_pt
    if result < 0:
        return 360 + result
    return result

ast.remove(best_ast)
angles_d = sorted(
    ((angle(best_ast, end), end) for end in ast),
    key=lambda x: (x[0], abs(best_ast[0] - x[1][0]) + abs(best_ast[1] - x[1][1]))
)
