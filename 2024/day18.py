from aoc_input import get_input
import aoc_lube
from utils import aoc_timer, parse_complex
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



i1 = '''5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
'''
 #   _____ ____  _____  ______   _    _ ______ _____  ______
 #  / ____/ __ \|  __ \|  ____| | |  | |  ____|  __ \|  ____|
 # | |   | |  | | |  | | |__    | |__| | |__  | |__) | |__
 # | |   | |  | | |  | |  __|   |  __  |  __| |  _  /|  __|
 # | |___| |__| | |__| | |____  | |  | | |____| | \ \| |____
 #  \_____\____/|_____/|______| |_|  |_|______|_|  \_\______|
 #
def print_maze(dims, g, path):
    for x in range(dims[0]):
        for y in range(dims[1]):
            if (x+1j*y) in path:
                print("O", end="")
            elif (x+1j*y) in g:
                print(".", end="")
            else:
                print("#", end="")
        print("")

def part1(inp, dims, nbbytes):
    total = 0
    G = nx.Graph()
    for x, y in itertools.product(range(dims[0]), range(dims[1])):
        for d in ALLDIRS:
            G.add_edge((x+1j*y), (x+1j*y+d))

    for r in inp.split("\n")[:nbbytes]:
        if r:
            x, y = map(int, r.split(","))
            G.remove_node(x+1j*y)
            pass

    print_maze(dims, G, nx.shortest_path(G,(0+0j), (dims[0]-1+1j*(dims[1]-1)),))
    return nx.shortest_path_length(G,(0+0j), (dims[0]-1+1j*(dims[1]-1)),)

def part2(inp, dims, nbbytes):
    G = nx.Graph()
    for x, y in itertools.product(range(dims[0]), range(dims[1])):
        for d in ALLDIRS:
            G.add_edge((x+1j*y), (x+1j*y+d))

    for r in inp.split("\n"):
        if r:
            x, y = map(int, r.split(","))
            G.remove_node(x+1j*y)
            _ =  nx.shortest_path_length(G,(0+0j), (dims[0]-1+1j*(dims[1]-1)),)
            # just use the debugger to check wht was the row that threw the exception LOL!
            pass

    return nx.shortest_path_length(G,(0+0j), (dims[0]-1+1j*(dims[1]-1)),)


sol1 = part1(i1, (7,7), 12)
print(sol1)

ii = aoc_lube.fetch(day=18, year=2024)
sol1 = part1(ii, (71,71), 1024)
print(sol1)

sol2 = part2(ii, (71,71), 1024)
print(sol2)
