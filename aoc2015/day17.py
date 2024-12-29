from aoc_lube import fetch
from functools import cache


s = fetch(2015, 17)

cont = tuple((int(r) for r in s.splitlines() if r))

@cache
def num_ways(rem, c,  rem_depth=999):
    if rem_depth <= 0:
        return 0
    if rem == 0:
        raise RuntimeError("dur dur")
    if not c or rem < 0:
        return 0
    if c[0] > rem:
        return num_ways(rem, c[1:], rem_depth)
    res =  sum([
        1 if rem == i*c[0] else num_ways(rem - i*c[0], c[1:], rem_depth-i) for i in range(2)])
#    print(f"{rem} {c} {res}")
    return res

print("part1: ", num_ways(150, cont))

for i in range(1, 100):
    res = num_ways(150, cont, i)
    if res:
        print("part2: ", res)
        break
