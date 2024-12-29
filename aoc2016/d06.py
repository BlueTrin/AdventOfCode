from aoc_lube import fetch
from collections import Counter

s = fetch(2016, 6)

xl = len([r for r in s.splitlines() if r])
yl = len(s.splitlines()[0])

rows = [r for r in s.splitlines() if r]
print(''.join([max(c:=Counter([rows[i][y] for i in range(xl) ]), key=c.get) for y in range(yl)]))

print(''.join([min(c:=Counter([rows[i][y] for i in range(xl) ]), key=c.get) for y in range(yl)]))
