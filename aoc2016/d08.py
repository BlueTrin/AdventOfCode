from aoc_lube import fetch
import re
import numpy as np

s = fetch(2016, 8)

sc = np.zeros((6, 50), dtype=int)
print(sc)

for r in s.splitlines():
    if r.startswith("rect"):
        a, b = map(int, re.findall(r"\d+", r))
        sc[:b, :a] = 1
    elif r.startswith("rotate row"):
        a, b = map(int, re.findall(r"\d+", r))
        sc[a] = np.roll(sc[a], b)
    elif r.startswith("rotate column"):
        a, b = map(int, re.findall(r"\d+", r))
        sc[:, a] = np.roll(sc[:, a], b)

print(np.sum(sc))

for row in sc:
    print("".join("#" if x else " " for x in row))
