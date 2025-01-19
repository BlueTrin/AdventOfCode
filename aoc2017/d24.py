from aoc_lube import fetch
from collections import deque

s = fetch(2017, 24)

parts = [tuple(map(int, x.split('/'))) for x in s.splitlines()]

assert len(set(parts)) == len(parts)

d = deque()
d.append((((0,0),),0))
max_strength = 0

longest = (0, 0)
while d:
    bridge, port = d.pop()
    added_bridge = False
    for p in parts:
        if p in bridge:
            continue
        if port in p:
            d.append((bridge + (p,), p[0] if p[1] == port else p[1]))
            added_bridge = True

    if not added_bridge:
        strength = sum(sum(p) for p in bridge)
        max_strength = max(max_strength, strength)

        long_bridge = (len(bridge), strength)
        longest = max(longest, long_bridge)

print(f"Part1: {max_strength}")
print(f"Part2: {longest[1]}")

