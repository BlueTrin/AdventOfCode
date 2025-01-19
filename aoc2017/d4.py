from aoc_lube import fetch

s = fetch(2017, 4)

print(s)

total = 0
for r in s.splitlines():
    words = r.split()
    if len(words) == len(set(words)):
        total += 1

print(f"Part1: {total}")

total = 0
for r in s.splitlines():
    words = r.split()
    words = [''.join(sorted(word)) for word in words]
    if len(words) == len(set(words)):
        total += 1

print(f"Part2: {total}")
