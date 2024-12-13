from adventofcode.inputs import get_input
from adventofcode.utils import aoc_timer, parse_complex
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


def parse_input(txt_inp):
    ''' put the stub to read the code here'''

    # complex reading:
    #   - coords_to_char: Dict[complex, str]
    #   - char_to_coordsset: Dict[str, Set[complex]]
    #   - max_coords: complex  -> max coordinates
    # coords_to_char, char_to_coordsset, max_coords = parse_complex(txt_inp)

    pass


 #   _____ ____  _____  ______   _    _ ______ _____  ______
 #  / ____/ __ \|  __ \|  ____| | |  | |  ____|  __ \|  ____|
 # | |   | |  | | |  | | |__    | |__| | |__  | |__) | |__
 # | |   | |  | | |  | |  __|   |  __  |  __| |  _  /|  __|
 # | |___| |__| | |__| | |____  | |  | | |____| | \ \| |____
 #  \_____\____/|_____/|______| |_|  |_|______|_|  \_\______|
 #


def part1(some_args):
    total = 0
    return total

def part2(some_args):
    total = 0
    return total


if __name__ == '__main__':
    txt_inp = '''............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''
    parsed = parse_input(txt_inp)
    sol1 = part1(*parsed)
    print(sol1)

    sol2 = part2(*parsed)
    print(sol2)
    # print_maze(nodes, coords, anti)

    txt_inp = get_input(, year=2024)
    parsed = parse_input(txt_inp)
    sol1 = part1(*parsed)
    print(sol1)

    sol2 = part2(*parsed)
    print(sol2)
