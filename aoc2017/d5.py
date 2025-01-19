from aoc_lube import fetch

s = fetch(2017, 5)

print(s)
offsets = [int(r) for r in s.splitlines()]

jumps = 0
pos = 0

while 0 <= pos < len(offsets):
    new_pos = pos + offsets[pos]
    offsets[pos] += 1
    pos = new_pos
    jumps += 1

print(f"Part1: {jumps}")


offsets = [int(r) for r in s.splitlines()]

jumps = 0
pos = 0

while 0 <= pos < len(offsets):
    new_pos = pos + offsets[pos]
    if offsets[pos] >= 3:
        offsets[pos] -= 1
    else:
        offsets[pos] += 1
    pos = new_pos
    jumps += 1

print(f"Part2: {jumps}")