from aoc_lube import fetch
import itertools

s = fetch(2020, 11)

def part1(s, part2=False, verbose=False):
    m = {}

    for iy, row in enumerate(s.splitlines()):
        for ix, c in enumerate(row):
            m[(ix, iy)] = c

    xm, ym = max(m.keys(), key=lambda x: x[0])[0], max(m.keys(), key=lambda x: x[1])[1]

    changed = True
    round = 0
    if verbose:
        print(f"Round {round}: {sum([v == '#' for v in m.values()])}")
        for y in range(ym + 1):
            print(''.join([m[(x, y)] for x in range(xm + 1)]))

    while changed:
        changed = False
        next_m = {}
        for x in range(xm+1):
            for y in range(ym+1):
                if part2:
                    neiocc = 0
                    for dx, dy in itertools.product([-1, 0, 1], repeat=2):
                        if (dx, dy) == (0, 0):
                            continue
                        n = 1
                        while (x+dx*n, y+dy*n) in m:
                            if m[(x+dx*n, y+dy*n)] == 'L':
                                break
                            elif m[(x+dx*n, y+dy*n)] == '#':
                                neiocc += 1
                                break
                            else:
                                n += 1

                else:
                    neiocc = sum([m.get((x+dx, y+dy)) == '#' for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)])
                if m[(x, y)] == 'L' and neiocc == 0:
                    next_m[(x, y)] = '#'
                    changed = True
                elif m[(x, y)] == '#' and ((not part2 and neiocc >= 4) or (part2 and neiocc >= 5)):
                    next_m[(x, y)] = 'L'
                    changed = True
                else:
                    next_m[(x, y)] = m[(x, y)]
        round += 1
        m = next_m
        if verbose:
            print(f"Round {round}: {sum([v == '#' for v in m.values()])}")
            for y in range(ym+1):
                print(''.join([m[(x, y)] for x in range(xm+1)]))
    return m

m = part1('''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL''', verbose=True)
print(f"Part1: {sum([v == '#' for v in m.values()])}")


m = part1(s)
print(f"Part1: {sum([v == '#' for v in m.values()])}")


m = part1(s, part2=True)
print(f"Part2: {sum([v == '#' for v in m.values()])}")
