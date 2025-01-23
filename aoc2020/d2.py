from aoc_lube import fetch
import re


s = fetch(2020, 2)

valid = 0
for r in s.splitlines():
    tokens = [x for x in re.split(r'[- :]', r) if x]
    lb, hb, c, pw = tokens

    valid += pw.count(c) in range(int(lb), int(hb)+1)


print(f"Part1: {valid}")
assert 483 == valid

valid = 0
for r in s.splitlines():
    tokens = [x for x in re.split(r'[- :]', r) if x]
    n1, n2, c, pw = tokens

    valid += (pw[int(n1)-1] == c) ^ (pw[int(n2)-1] == c)

print(f"Part2: {valid}")
assert 482 == valid
