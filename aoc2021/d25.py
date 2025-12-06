from aoc_lube import fetch
from utils.utils import Point, E, S

s = fetch(2021, 25)

# s = '''v...>>.vv>
# .vv>>.vv..
# >>.>v>...v
# >>v>>.>.v.
# v>v.vv.v..
# >.>>..v...
# .vv..>.>v.
# v.v..>>v.v
# ....v..v.>'''
m = {}
max_y = 0
max_x = 0
for y, row in enumerate(s.splitlines()):
    max_y = max(y, max_y)
    for x, c in enumerate(row):
        if c != '.':
            m[Point(x, y)] = c
        max_x = max(x, max_x)
DIR = {
    '>': E,
    'v': S,
}
def play(m):
    moved = 0
    for c in ['>', 'v']:
        new_m = {}
        for pt, v in m.items():
            if v != c:
                new_m[pt] = v
                continue

            new_pt = pt + DIR[c]
            new_pt = Point(new_pt.x % (max_x + 1), new_pt.y % (max_y + 1))

            if new_pt not in m:
                moved += 1
                new_m[new_pt] = v
            else:
                new_m[pt] = v
        m = new_m
    return m, moved

def p(m):
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if Point(x, y) in m:
                print(m[Point(x, y)], end='')
            else:
                print('.', end='')
        print()

turn = 0
while True:
    turn += 1
    new_m, moved = play(m)
    assert len(new_m) == len(m)
    m = new_m

    if moved == 0:
        break

print(turn)