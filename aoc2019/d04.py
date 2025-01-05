from aoc_lube import fetch
import re

s = fetch(2019, 4)

n1, n2 = map(int, s.split('-'))

total = 0
for c in range(n1, n2+1):
    s = str(c)
    if len(s) ==6 and sorted(s) == list(s) and re.match(r'.*(\d)\1.*', s):
        total += 1

print(total)
total = 0
for c in range(n1, n2+1):
    s = str(c)
    if len(s) ==6 and sorted(s) == list(s) and re.match(r'.*(\d)(?<!(?=\1)..)\1(?!\1).*', s):
        total += 1

print(total)
