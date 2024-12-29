from aoc_lube import fetch

s = fetch(2016, 1)

d = 1j
pos = 0
seen = set()
seen.add(pos)
for r in s.split(', '):
    if r[0] == 'R':
        d *= 1j
    else:
        d *= -1j

    for i in range(1, int(r[1:])+1):
        new_pos = pos + d * i
        if new_pos in seen:
            print(f"part2: {new_pos} {abs(new_pos.real) + abs(new_pos.imag)}")
        seen.add(new_pos)
    pos =  pos + d * int(r[1:])

print(f"part1: {pos} {abs(pos.real) + abs(pos.imag)}")
