from os import utime

from utils2018.aoc_input import get_input
from utils2018 import aoc_timer, parse_complex
from typing import Dict, List, Tuple, Set
import math
import itertools
import networkx as nx
import scipy
import numpy as np

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

#   _____ ______ _   _ ______ _____            _
#  / ____|  ____| \ | |  ____|  __ \     /\   | |
# | |  __| |__  |  \| | |__  | |__) |   /  \  | |
# | | |_ |  __| | . ` |  __| |  _  /   / /\ \ | |
# | |__| | |____| |\  | |____| | \ \  / ____ \| |____
#  \_____|______|_| \_|______|_|  \_\/_/    \_\______|
#

N = -1j
S = 1j
W = -1
E = 1

NW = N + W
NE = N + E
SW = S + W
SE = S + E

ALLDIRS = [N, S, E, W]

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
 #   _____ ____  _____  ______   _    _ ______ _____  ______
 #  / ____/ __ \|  __ \|  ____| | |  | |  ____|  __ \|  ____|
 # | |   | |  | | |  | | |__    | |__| | |__  | |__) | |__
 # | |   | |  | | |  | |  __|   |  __  |  __| |  _  /|  __|
 # | |___| |__| | |__| | |____  | |  | | |____| | \ \| |____
 #  \_____\____/|_____/|______| |_|  |_|______|_|  \_\______|
 #


def part1(inp):
    total = 0
    co_to_c, c_to_co, dims = parse_complex(inp)
    start = next(iter(c_to_co['S']))
    end = next(iter(c_to_co['E']))
    DG = nx.DiGraph()
    for p in c_to_co['.'] | c_to_co['E'] | c_to_co['S']:
        for d in ALLDIRS:
            if p+d == end:
                dest = end
            else:
                dest = (p+d, d)
            DG.add_edge((p, d), dest, weight=1)  # don't bother checking for walls, we like to crash into them lol
            DG.add_edge((p, d), (p, d*1j), weight=1000)
            DG.add_edge((p, d), (p, d*-1j), weight=1000)

    short_path_len = nx.shortest_path_length(DG, (start, E), end, weight="weight")
    seen = set()
    for path in nx.all_shortest_paths(DG, (start, E), end, weight="weight"):
        for n in path:
            seen.add(n if isinstance(n, complex) else n[0])
    return short_path_len, len(seen)

def part2(some_args):
    total = 0
    # oh well I didn't need this for part 2
    return total


sol1 = part1(i1)
print(sol1)

ii = get_input(16, year=2024)
sol1 = part1(ii)
print(sol1)

sol2 = part2(i1)
print(sol2)
# print_maze(nodes, coords, anti)

sol2 = part2(ii)
print(sol2)
