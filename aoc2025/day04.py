from aoc_lube import fetch
import math
from functools import cache
import numpy as np
from utils.utils import (Point, parse_point, EIGHTDIRS)
import copy


def removable(co, co_to_c):
    neighbours = 0
    for d in EIGHTDIRS:
        if co_to_c.get(co + d, '.') == '@':
            neighbours += 1
        if neighbours >= 4:
            break

    return neighbours < 4


def part1(c_to_cos, co_to_c):
    res1 = 0
    for co in c_to_cos['@']:
        if removable(co, co_to_c):
            res1 += 1
    return res1

def main():
    s = fetch(2025, 4)

    co_to_c, c_to_cos, lens = parse_point(s)
    res1 = part1(c_to_cos, co_to_c)

    res2 = 0
    has_removed = True
    while has_removed:
        has_removed = False
        check_list = copy.copy(c_to_cos['@'])
        for co in check_list:
            if removable(co, co_to_c):
                res2 += 1
                has_removed = True
                c_to_cos['@'].remove(co)
                co_to_c[co] = '.'

    print(res1)
    print(res2)

if __name__ == "__main__":
    main()
