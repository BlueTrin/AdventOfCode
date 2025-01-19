from aoc_lube import fetch
import math
from functools import cache
import numpy as np

s = fetch(2017, 3)
# 37  36  35  34  33  32 31
# 38  17  16  15  14  13 30
# 39  18   5   4   3  12 29
# 40  19   6   1   2  11 28
# 41  20   7   8   9  10 27
# 42  21   22  23  24 25 26
# 43  44  45  46  47  48 49 <- ALWAYS THE SIZE OF THE SQUARE

def level(n) -> int:
    # the square containing n is its square root rounded up
    return math.ceil(n**0.5) | 1

def pos(n) -> int:
    if n ==1:
        return 0
    # the position of n in its square
    lvl = level(n)
    to_level_mid =  (n - (lvl**2 - lvl//2)) % (lvl-1)

    if to_level_mid > lvl // 2:
        to_level_mid = abs(to_level_mid - (lvl - 1))

    return to_level_mid + lvl//2

assert pos(1) == 0
assert level(12) == 5
assert pos(12) == 3
assert level(23) == 5
assert pos(23) == 2
assert pos(1024) == 31

assert pos(49) == 6
assert pos(37) == 6
assert pos(31) == 6
assert pos(42) == 5
assert pos(43) == 6
assert pos(44) == 5

print(f"Part1: {pos(int(s))}")

# 147  142  133  122   59
# 304    5    4    2   57
# 330   10    1    1   54
# 351   11   23   25   26
# 362  747  806--->   ...

# https://oeis.org/A141481
l = 11
m = np.zeros((l, l))


m[l//2, l//2] = 1
lvl = 1
while lvl < l//2:
    # right
    x = l//2 + lvl
    for y in range(l//2 + lvl - 1, l//2 - lvl - 1, -1):
        m[y, x] = m[y-1, x-1] + m[y-1, x] + m[y-1, x+1] + m[y, x-1] + m[y, x+1] + m[y+1, x-1] + m[y+1, x] + m[y+1, x+1]

    # top
    y = l//2 - lvl
    for x in range(l//2 + lvl, l//2 - lvl - 1, -1):
        m[y, x] = m[y-1, x-1] + m[y-1, x] + m[y-1, x+1] + m[y, x-1] + m[y, x+1] + m[y+1, x-1] + m[y+1, x] + m[y+1, x+1]

    # left
    x = l//2 - lvl
    for y in range(l//2 - lvl, l//2 + lvl + 1):
        m[y, x] = m[y-1, x-1] + m[y-1, x] + m[y-1, x+1] + m[y, x-1] + m[y, x+1] + m[y+1, x-1] + m[y+1, x] + m[y+1, x+1]

    # bottom
    y = l//2 + lvl
    for x in range(l//2 - lvl, l//2 + lvl + 1):
        m[y, x] = m[y-1, x-1] + m[y-1, x] + m[y-1, x+1] + m[y, x-1] + m[y, x+1] + m[y+1, x-1] + m[y+1, x] + m[y+1, x+1]

    if m[y, x] > int(s):
        p1 = min([elem for elem in np.nditer(m) if elem > int(s)])
        print(f"Part2: {p1}")
        break
    lvl += 1