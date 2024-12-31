from aoc_lube import fetch
from networkx.algorithms.community.quality import partition_quality

s = fetch(2016, 20)

blist = list()
print(s)

for r in s.splitlines():
    if r is None:
        continue

    a, b = r.split('-')
    blist.append((int(a), int(b)))

blist.append((4294967296, 4294967297))
blist.sort()

part1 = None
curr = 0
idx = 0
valid_ips = 0

while True:
    if curr > 4294967295:
        break
    if blist[idx][0] <= curr <= blist[idx][1]:
        curr = blist[idx][1] + 1
        idx += 1
    elif curr > blist[idx][1]:
        idx += 1
    else:
        if part1 is None:
            part1 = curr
            print("part1:", part1)
        valid_ips += blist[idx][0] - curr
        curr = blist[idx][1] + 1

print(valid_ips)
