from aoc_lube import fetch
import math
from functools import cache
import numpy as np
from utils.utils import (Point, parse_point, EIGHTDIRS)
import copy

def is_fresh(ing, fresh_range_lst):
    for idmin, idmax in fresh_range_lst:
        if idmin <= int(ing) <= idmax:
            return True
    return False

def part1(fresh_range_lst, ingredients):
    res = 0
    for ing in ingredients:
        if is_fresh(ing, fresh_range_lst):
            res += 1
    return res


def part2(fresh_range_lst):
    res = 0
    iteration = 0

    has_merged = True
    while has_merged:
        has_merged = False
        used_ids = set()
        merged_lst = []
        for i, r_it1 in enumerate(fresh_range_lst):
            if i in used_ids:
                continue
            for j in range(i+1, len(fresh_range_lst)):
                if j in used_ids:
                    continue
                r_it2 = fresh_range_lst[j]
                if r_it2[0] <= r_it1[0] <= r_it2[1] or r_it2[0] <= r_it1[1] <= r_it2[1] or \
                        r_it1[0] <= r_it2[0] <= r_it1[1] or r_it1[0] <= r_it2[1] <= r_it1[1]:
                    merged_lst.append( (min(r_it1[0], r_it2[0]), max(r_it1[1], r_it2[1])) )
                    used_ids.add(i)
                    used_ids.add(j)
                    has_merged = True
                    break
            else:
                merged_lst.append(r_it1)
                used_ids.add(i)

            if has_merged and len(merged_lst) >= len(fresh_range_lst):
                print("Error in merging")

        fresh_range_lst = merged_lst
        iteration += 1
        # assert not has_merged or len(fresh_range_lst) < len(used_ids)

    for rmin, rmax in merged_lst:
        res += rmax - rmin + 1

    return res

def main():
    s = fetch(2025, 5)

    fresh_range_lst = []
    fresh_range_str, ingredients = s.split('\n\n')
    for line in fresh_range_str.splitlines():
        idmin, idmax = line.split('-')
        fresh_range_lst.append( (int(idmin), int(idmax)) )
    ingredients = ingredients.splitlines()

    res1 = part1(fresh_range_lst, ingredients)

    print(res1)

    res2 = part2(fresh_range_lst)
    print(res2)

if __name__ == "__main__":
    main()
