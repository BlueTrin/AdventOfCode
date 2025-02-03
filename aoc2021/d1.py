from aoc_lube import fetch

s = fetch(2021, 1)

measurements = [int(r) for r in s.splitlines()]

print(f"Part1: {sum([v2 > v1 for v1, v2 in zip(measurements, measurements[1:])])}")

triplets = [tuple(x) for x in zip(measurements, measurements[1:], measurements[2:])]

print(f"Part2: {sum([sum(v2) > sum(v1) for v1, v2 in zip(triplets, triplets[1:])])}")