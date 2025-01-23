from aoc_lube import fetch
import itertools

s = fetch(2020, 1)
# print(s)

for i1, i2 in itertools.combinations(map(int, s.splitlines()), 2):
    if i1 + i2 == 2020:
        print(f"Part1: {i1*i2}")
        break

for i1, i2, i3 in itertools.combinations(map(int, s.splitlines()), 3):
    if i1 + i2 + i3 == 2020:
        print(f"Part2: {i1*i2*i3}")
        break
