from aoc_lube import fetch
import math
from functools import cache
import numpy as np
def main():
    s = fetch(2025, 1)

    print(s)
    start = 50
    res = 0
    res2 = 0
    for r in s.splitlines():
        if r[0] == 'L':
            chg = - int(r[1:])
        elif r[0] == 'R':
            chg = int(r[1:])

        if chg < 0:
            while chg < -99:
                chg += 100
                res2 += 1

            if start + chg <= 0 < start:
                res2 += 1
        elif chg > 0:
            while chg > 100:
                chg -= 100
                res2 += 1
            if start < 100 <= start + chg:
                res2 += 1
        start = (start + chg) % 100
        if start == 0:
            res += 1

    print(res)
    print(res2)

if __name__ == "__main__":
    main()