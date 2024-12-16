from aoc_input import get_input
from utils import aoc_timer, parse_complex
from typing import Dict, List, Tuple, Set
import math
import itertools

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


#  _____  ______          _____    _____ _   _ _____  _    _ _______
# |  __ \|  ____|   /\   |  __ \  |_   _| \ | |  __ \| |  | |__   __|
# | |__) | |__     /  \  | |  | |   | | |  \| | |__) | |  | |  | |
# |  _  /|  __|   / /\ \ | |  | |   | | | . ` |  ___/| |  | |  | |
# | | \ \| |____ / ____ \| |__| |  _| |_| |\  | |    | |__| |  | |
# |_|  \_\______/_/    \_\_____/  |_____|_| \_|_|     \____/   |_|

import re
def parse_input(txt_inp):
    ''' put the stub to read the code here'''
    res = []
    for r in txt_inp.splitlines():
        if r:
            _, x, y, vx, vy = re.split(r"[^(\d\-)]+", r)
            res.append((int(x) + 1j * int(y), int(vx) + 1j * int(vy)))
    if len(txt_inp.splitlines())< 20:
        d = (11, 7)
    else:
        d = (101,103)
    return res, d


 #   _____ ____  _____  ______   _    _ ______ _____  ______
 #  / ____/ __ \|  __ \|  ____| | |  | |  ____|  __ \|  ____|
 # | |   | |  | | |  | | |__    | |__| | |__  | |__) | |__
 # | |   | |  | | |  | |  __|   |  __  |  __| |  _  /|  __|
 # | |___| |__| | |__| | |____  | |  | | |____| | \ \| |____
 #  \_____\____/|_____/|______| |_|  |_|______|_|  \_\______|
 #


def part1(robots, dim):
    total = 0
    quad = tuple( (x -1)//2 for x in dim)
    quadcount = [0] * 4
    for pos, di in robots:
        final = pos + di * 100
        final = final.real % dim[0] + 1j * (final.imag % dim[1])
        if quad[0] != final.real and quad[1] != final.imag:
            quadpos = 0
            if quad[0] < final.real:
                quadpos += 1
            if quad[1] < final.imag:
                quadpos += 2

            quadcount[quadpos] += 1


    return math.prod(quadcount)

def simulate(pos, di, turns, dim):
    final = pos + di * turns
    final = final.real % dim[0] + 1j * (final.imag % dim[1])
    return final

def part2(robots, dim):
    total = 0

    turn = 1
    while True:
        seen = set()
        for pos, di in robots:
            final = simulate(pos, di, turn, dim)
            seen.add(final)

        if len(seen) == len(robots):
            return turn
        turn += 1


txt_inp = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''
parsed = parse_input(txt_inp)
sol1 = part1(*parsed)
print(sol1)

# sol2 = part2(*parsed)
# print(sol2)
# print_maze(nodes, coords, anti)

txt_inp = get_input(14, year=2024)
parsed = parse_input(txt_inp)
sol1 = part1(*parsed)
print(sol1)

sol2 = part2(*parsed)
print(sol2)
