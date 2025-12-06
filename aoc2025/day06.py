from aoc_lube import fetch
import math
from functools import cache
import numpy as np
from utils.utils import (Point, parse_point, EIGHTDIRS)
import copy
import logging
from operator import mul, add
from functools import reduce

logging.basicConfig(level=logging.INFO)

def part1(elts):
    res = 0
    for ipb, elt_lst in elts.items():
        if elt_lst[-1] == '*':
            op = mul
        elif elt_lst[-1] == '+':
            op = add
        else:
            raise ValueError(f"Unknown operation{elt_lst[-1]}")
        v = reduce(op, [int(x) for x in elt_lst[:-1]])
        res += v
    return res


def part2(m):
    res = 0

    i_start = 0

    while i_start < len(m):
        # find non space col
        while i_start < len(m):
            for j in range(len(m[i_start])):
                if m[i_start][j] == ' ':
                    continue
                else:
                    break
            else:
                # found only spaces
                i_start += 1
                continue

            # fond non space
            break

        i_end = i_start + 1
        while i_end < len(m):
            for j in range(len(m[i_end])):
                if m[i_end][j] == ' ':
                    continue
                else:
                    break
            else:
                # found only spaces
                break

            # fond non space
            i_end +=1
            continue

        op_ch = m[i_start][len(m[i_start])-1]
        if op_ch == '*':
            op = mul
        elif op_ch == '+':
            op = add
        else:
            raise ValueError(f"Unknown operation{op_ch}")

        col_vals = []
        indexes = sorted(m[0].keys())
        for col in range(i_start, i_end):
            colval = 0
            for row in indexes[:-1]:
                if m[col][row] != ' ':
                    colval *= 10
                    colval += int(m[col][row])
            col_vals.append(colval)

        v = reduce(op, [v for v in col_vals if v != 0])
        logging.info(f"Computed value for cols {i_start}-{i_end}: {v} = {col_vals} with op {op_ch}")
        res += v
        i_start = i_end+1

    return res

def main():
    s = fetch(2025, 6)
#     s = '''123 328  51 64
#  45 64  387 23
#   6 98  215 314
# *   +   *   +  '''
    elts = {}
    for j, line in enumerate(s.splitlines()):
        for i, ch in enumerate([x for x in line.split(' ') if x != '']):
            if i not in elts:
                elts[i] = []
            elts[i].append(ch)

    res1 = part1(elts)
    print(res1)

    m = {}
    for j, line in enumerate(s.splitlines()):
        for i, ch in enumerate(line):
            if i not in m:
                m[i] = {}
            m[i][j] = ch

    res2 = part2(m)
    print(res2)

if __name__ == "__main__":
    main()
