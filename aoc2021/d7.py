from aoc_lube import fetch
import math
import numpy as np
from functools import cache

s = fetch(2021, 7)
# s = "16,1,2,0,4,2,7,1,2,14"
pos = [int(x) for x in s.split(',')]
avg = int(np.median(pos))
s = sum([abs(x - avg) for x in pos])
s2 = sum([abs(x - (avg+1)) for x in pos])
print(f"Part1: {min(s, s2)}")

@cache
def fuel(x):
    if x == 0:
        return 0
    else:
        return x + fuel(x-1)

h = sum([fuel(abs(x - (avg+1))) for x in pos])
m = sum([fuel(abs(x - avg)) for x in pos])
l = sum([fuel(abs(x - (avg-1))) for x in pos])

while h < m or l < m:
    if h < m:
        avg += 1
        m = h
        l = m
        h = sum([fuel(abs(x - (avg+1))) for x in pos])
    if l < m:
        avg -= 1
        m = l
        h = m
        l = sum([fuel(abs(x - (avg-1))) for x in pos])

print(f"Part2: {m}")

