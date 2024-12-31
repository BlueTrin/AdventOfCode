from aoc_lube import fetch
import re
from math import lcm


s = fetch(2016, 15)

discs = []

for i, r in enumerate(s.splitlines()):
    if r is None:
        continue

    m = re.match(r'Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+).', r)
    if m is None:
        raise RuntimeError("Invalid input")

    discs.append((int(m.group(2)), int(m.group(3))))


print(discs)
rng = lcm(*[p[0] for p in discs])
good_pos = [set(range((p[0]- (i+1) - p[1])%p[0], rng, p[0]) )for i, p in enumerate(discs)]

print(set.intersection(*good_pos))
# 122319 is too high

discs.append((11, 0))
rng = lcm(*[p[0] for p in discs])
good_pos = [set(range((p[0]- (i+1) - p[1])%p[0], rng, p[0]) )for i, p in enumerate(discs)]

print(set.intersection(*good_pos))
