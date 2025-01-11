from aoc_lube import fetch
from intcode import Intcode
from utils.utils import Point

s = fetch(2019, 11)

program = list(map(int, s.strip().split(',')))

ship = {}
pos = Point(0, 0)
dir = Point(0, -1)

c = Intcode(program)
DEFAULTCOL = 1
c.input.append(ship.get(pos, DEFAULTCOL))
while not c.halted:
    c.run()
    paint, rot = c.output.popleft(), c.output.popleft()
    print(f"output from int comp 0  :{paint}")
    print(f"output from int comp 0  :{rot}")

    if pos == Point(-25, -26):
        raise RuntimeError("should not be here")
    ship[pos] = paint
    if rot == 0:
        dir = dir.rotate(-90)
    elif rot == 1:
        dir = dir.rotate(90)
    else:
        raise Exception(f'Unknown rotation {rot}')

    pos += dir
    c.input.append(ship.get(pos, DEFAULTCOL))
    print("waiting input")
    # print(paint, rot)

print(f"part 1: {len(ship)}")


min_x = min(p.x for p in ship) - 1
max_x = max(p.x for p in ship) + 1
max_y = max(p.y for p in ship) + 1
min_y = min(p.y for p in ship) - 1

for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x +1):
        print('#' if ship.get(Point(x, y), 0) else ' ', end='')
    print()

# EFCKUEGC