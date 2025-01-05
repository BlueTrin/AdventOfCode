from aoc_lube import fetch, submit
from utils2018 import aoc_timer, parse_complex
from typing import Dict, List, Tuple, Set
import math
import itertools
import networkx as nx
import scipy
import numpy as np
from collections import deque, defaultdict
from heapq import heappush, heappop
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# GCD -> math.gcd

# all combinations (no order):
# >>> list(itertools.combinations([1,2,3], 2))
# [(1, 2), (1, 3), (2, 3)]

# all permutations
# >>> list(itertools.permutations([1,2,3], 2))
# [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# product
# >>> list(itertools.product([1,2,3], repeat=2))
# [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]

# GENERAL DEFINITIONS # GENERAL DEFINITIONS # GENERAL DEFINITIONS # GENERAL DEFINITIONS # GENERAL DEFINITIONS # GENERAL DEFINITIONS

N = -1j
S = 1j
W = -1
E = 1

FOURDIRS = [N, S, E, W]

NW = N + W
NE = N + E
SW = S + W
SE = S + E

def print_maze(nodes, coords, anti ):
    s = ""
    for y in range(int(coords.imag)):
        for x in range(int(coords.real)):
            pt = x + y * 1j
            if pt in anti:
                s += "#"
            else:
                is_node = False
                for c, node_pts in nodes.items():
                    if pt in node_pts:
                        s += c
                        is_node = True
                        break
                if not is_node:
                    s += "."

        s += "\n"
    print(s)


i1 = '''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
'''
 #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE
def map_dst(start, allowed):
    dst_map = {start: 0}
    boundary = dst_map
    has_written = True
    curr_dst = 0
    while has_written:
        has_written = False
        curr_dst += 1
        new_boundary = {}
        for c in boundary:
            for d in FOURDIRS:
                dst = c+d
                if dst in allowed and dst not in dst_map:
                    new_boundary[dst] = curr_dst
                    has_written = True
        dst_map.update(new_boundary)
        boundary = new_boundary
    return dst_map

def cheats(start_dst,end_dst, cheat_pos, shortest_len):
    sols = defaultdict(set)
    for c in cheat_pos:
        for d in FOURDIRS:
            start = c+d
            end = c-d
            cheat_len = start_dst.get(start, math.inf) + end_dst.get(end, math.inf) + 2
            if cheat_len < shortest_len:
                sols[shortest_len-cheat_len].add(c)
    return sols

def cheat_len(start_dst,end_dst, max_cheat_len, shortest_len):
    sols = defaultdict(set)
    for s in start_dst:
        for e in end_dst:
            cheat_len = (abs(e.imag - s.imag) + abs(e.real - s.real))
            if cheat_len > max_cheat_len:
                continue
            cheat_dst = start_dst[s] + end_dst[e] + cheat_len
            if cheat_dst < shortest_len:
                sols[shortest_len -cheat_dst].add((s, e))
    return sols

def part1(inp, min_save, max_cheat_len=2, debug=False):
    total = 0
    _, c_to_cos, lens = parse_complex(inp)
    start = list(c_to_cos["S"])[0]
    end = list(c_to_cos["E"])[0]
    start_dst = map_dst(start, c_to_cos['.']|c_to_cos['E']|c_to_cos['S'])
    end_dst = map_dst(end, c_to_cos['.']|c_to_cos['E']|c_to_cos['S'])
    shortest_len = start_dst[end]

#    sols = cheats(start_dst,end_dst, c_to_cos['#'], shortest_len)
    sols = cheat_len(start_dst,end_dst, max_cheat_len, shortest_len)
    for k in sorted(sols.keys()):
        if k >= min_save:
            total += len(sols[k])
            if debug:
                logger.info(f"cheat {k}: {len(sols[k])} cheats")
    return total

def part2(some_args):
    total = 0
    return total

# RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE

# sol1 = part1(i1, 0, 2, debug=True)
# print(sol1)
#
ii = fetch(2024, 20)
# sol1 = part1(ii, 100, 2)
# print(sol1)

sol2 = part1(i1, 50, 20, debug=True)
print(sol2)
# print_maze(nodes, coords, anti)

sol2 = part1(ii, 100, 20)
print(sol2)
