from aoc_lube import fetch
import math
from functools import cache
import numpy as np

def max_part1(idstr, len_limit):
    res = 0
    seq = [int(c) for c in idstr]
    for i in reversed(range(len_limit)):
        res *= 10
        digit = max(seq[:len(seq)-i])
        seq = seq[seq.index(digit)+1:]
        res += digit
    return res

def main():
    s = fetch(2025, 3)
    res1 = 0
    res2 = 0
    for line in s.splitlines():
        res1 += max_part1(line, 2)
        res2 += max_part1(line, 12)

    print(res1)
    print(res2)




if __name__ == "__main__":
    main()