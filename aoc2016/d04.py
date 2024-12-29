from aoc_lube import fetch
import re
from collections import Counter

s = fetch(2016, 4)

total = 0
for r in s.splitlines():
    if not r:
        continue
    m = re.match(r"([a-z-]+)-(\d+)\[([a-z]+)\]", r)
    name, sector, checksum = m.groups()
    count = Counter(name.replace('-', ''))
    chk = ''.join([x[0] for x in sorted(count.items(), key=lambda x: (-x[1], x[0]))][:5])
    if chk == checksum:
        total += int(sector)

print("part1:", total)

for r in s.splitlines():
    if not r:
        continue
    m = re.match(r"([a-z-]+)-(\d+)\[([a-z]+)\]", r)
    name, sector, checksum = m.groups()
    sector = int(sector)
    name = name.replace('-', ' ')

    for i, c in enumerate(name):
        if c == ' ':
            continue
        name = name[:i] + chr((ord(c) - ord('a') + sector) % 26 + ord('a')) + name[i+1:]

    if 'north' in name:
        print("part2:", sector , name)
        break