from aoc_lube import fetch

s = fetch(2016, 3)

total = 0
for r in s.splitlines():
    a, b, c = map(int, r.split())
    if a + b > c and a + c > b and b + c > a:
        total += 1

print(f"part1: {total}")
triangles = []
for r in zip(s.splitlines()[::3], s.splitlines()[1::3], s.splitlines()[2::3]):
    for t in zip(*[map(int, x.split()) for x in r]):
        triangles.append(t)
total = 0
for t in triangles:
    a, b, c = t
    if a + b > c and a + c > b and b + c > a:
        total += 1

print(f"part2: {total}")