from aoc_lube import fetch
import re
s = fetch(2016, 11)

floors = []
for ifloor, r in enumerate(s.splitlines()):
    _, details = r.split("contains")
    if 'nothing' in details:
        floors.append(0)
    else:
        floors.append(len([x for x in re.split(r',|and', details) if x.strip()]))

total = 0
for i in range(1, len(floors)):
    # move to the floor above
    total += (sum(floors[:i]) - 2) * 2 + 1

print("Part 1:", total)
floors[0] += 4

total = 0
for i in range(1, len(floors)):
    # move to the floor above
    total += (sum(floors[:i]) - 2) * 2 + 1

print("Part 2:", total)
