from aoc_lube import fetch, submit
from utils import aoc_timer, parse_complex
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
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
'''
 #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE  #  CODE HERE

def part1(inp):
    total = 0
    # co_to_c, c_to_cos, lens = parse_complex(ex_txt_input)
    return total

def part2(some_args):
    total = 0
    return total

# RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE # RUN STUFF HERE

sol1 = part1(i1)
print(sol1)

ii = fetch(2024, 16)
sol1 = part1(ii)
print(sol1)

sol2 = part2(i1)
print(sol2)
# print_maze(nodes, coords, anti)

sol2 = part2(ii)
print(sol2)
