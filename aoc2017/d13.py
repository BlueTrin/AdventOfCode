from aoc_lube import fetch

s = fetch(2017, 13)

sev = 0
layers = {}
for r in s.splitlines():
    depth, range_ = map(int, r.split(': '))
    layers[depth] = range_

for depth, range_ in layers.items():
    if depth % ((range_ - 1) * 2) == 0:
        sev += depth * range_

print(f"Part1: {sev}")

delay = 0
while any((depth + delay) % ((range_ - 1) * 2) == 0 for depth, range_ in layers.items()):
    delay += 1

print(f"Part2: {delay}")
