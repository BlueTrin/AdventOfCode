from aoc_lube import fetch

data = fetch(2021, 11)

EIGHTDIRS = [(dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx, dy) != (0, 0)]
d = {(ix, iy): int(c) for iy, s in enumerate(data.splitlines()) for ix,c in enumerate(s)}
pass

p1 = 0
round = 0
while True:
    round += 1
    flashes = 0
    for (x, y) in d:
        d[x, y] += 1

    has_flashes = True
    while has_flashes:
        has_flashes = False
        for (x, y) in d:
            if d[x, y] > 9:
                has_flashes = True
                flashes += 1
                d[x, y] = -20
                for dx, dy in EIGHTDIRS:
                    if (x+dx, y+dy) in d:
                        d[x+dx, y+dy] += 1

    if round <= 100:
        p1 += flashes
    for (x, y) in d:
        if d[x, y] < 0:
            d[x, y] = 0

    if flashes == len(d):
        print(f"p2 {round}")
        break
print(f"Part1: {p1}")