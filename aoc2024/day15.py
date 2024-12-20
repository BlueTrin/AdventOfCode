small_inp = '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<'''

big_inp = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^'''

from utils.aoc_input import get_input
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

C_TO_DIR = {
    'v': S,
    '^': N,
    '<': W,
    '>': E,
}

def print_maze(maze, coords):
    s = ""
    for y in range(int(coords[1])):
        for x in range(int(coords[0])):
            pt = x + y * 1j
            s += maze[pt]

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
    txt_inp2, txt_inp3 = txt_inp.split("\n\n")
    # complex reading:
    #   - coords_to_char: Dict[complex, str]
    #   - char_to_coordsset: Dict[str, Set[complex]]
    #   - max_coords: complex  -> max coordinates
    coords_to_char, char_to_coordsset, max_coords = parse_complex(txt_inp2)

    dir_lst = [C_TO_DIR[c] for line in txt_inp3.splitlines() for c in line]
    return list(char_to_coordsset['@'])[0], coords_to_char, max_coords, dir_lst


 #   _____ ____  _____  ______   _    _ ______ _____  ______
 #  / ____/ __ \|  __ \|  ____| | |  | |  ____|  __ \|  ____|
 # | |   | |  | | |  | | |__    | |__| | |__  | |__) | |__
 # | |   | |  | | |  | |  __|   |  __  |  __| |  _  /|  __|
 # | |___| |__| | |__| | |____  | |  | | |____| | \ \| |____
 #  \_____\____/|_____/|______| |_|  |_|______|_|  \_\______|
 #


def part1(pos, coords_to_char, max_coords, dir_lst, debug=False):
    total = 0
    for d in dir_lst:
        shift_len = 1
        while coords_to_char[pos + shift_len * d] not in ['#', '.']:
            shift_len +=1
        if coords_to_char[pos + shift_len * d] == '#':
            shift_len = 0
        else:
            coords_to_char[pos+d], coords_to_char[pos+d*shift_len] = coords_to_char[pos+d*shift_len], coords_to_char[pos+d]
            coords_to_char[pos + d], coords_to_char[pos] = coords_to_char[pos], coords_to_char[pos+d]
            pos += d
        if debug:
            print(f"after processing dir={d}\n")
            print_maze(coords_to_char, max_coords)
            input()
    for pos_c,c  in coords_to_char.items():
        if c == 'O':
            total +=  pos_c.imag* 100 + pos_c.real
    return total


def do_shift(pos, d, co_to_c):
    assert d in [N, S]
    assert co_to_c[pos] != "#"
    if co_to_c[pos] == ".":
        return True
    elif co_to_c[pos] == "[":
        assert co_to_c[pos + E] == "]"
        do_shift(pos + d, d, co_to_c)
        do_shift(pos + E + d, d, co_to_c)
        assert (co_to_c[pos + d ], co_to_c[pos + d +E]) == ('.', '.')
        co_to_c[pos + d ], co_to_c[pos ] = co_to_c[pos ], co_to_c[pos + d ]
        co_to_c[pos + d + E], co_to_c[pos + E] = co_to_c[pos + E], co_to_c[pos + d + E]
    elif co_to_c[pos] == "]":
        assert co_to_c[pos + W] == "["
        do_shift(pos + d, d, co_to_c)
        do_shift(pos + W + d, d, co_to_c)
        assert (co_to_c[pos + d ], co_to_c[pos + d +W]) == ('.', '.')
        co_to_c[pos + d ], co_to_c[pos ] = co_to_c[pos ], co_to_c[pos + d ]
        co_to_c[pos + d + W], co_to_c[pos + W] = co_to_c[pos + W], co_to_c[pos + d + W]
    elif co_to_c[pos] == "@":
        do_shift(pos + d, d, co_to_c)
        co_to_c[pos + d ], co_to_c[pos ] = co_to_c[pos ], co_to_c[pos + d ]
    else:
        raise RuntimeError("ERR")


def can_shift(pos, d, co_to_c):
    assert d in [N, S]
    if co_to_c[pos] == ".":
        return True
    elif co_to_c[pos] == "[":
        assert co_to_c[pos+E] == "]"
        return can_shift(pos+d, d, co_to_c) and can_shift(pos+E+d, d, co_to_c)
    elif co_to_c[pos] == "]":
        assert co_to_c[pos+W] == "["
        return can_shift(pos+d, d, co_to_c) and can_shift(pos+W+d, d, co_to_c)
    elif co_to_c[pos] == "#":
        return False
    elif co_to_c[pos] == "@":
        return can_shift(pos + d, d, co_to_c)
    else:
        raise RuntimeError("BOO")

def part2(pos, coords_to_char, max_coords, dir_lst,debug=False):
    total = 0
    temp = {}
    orig = coords_to_char
    for coord, c in coords_to_char.items():
        if c == '#':
            temp[coord.real*2 + 1j * coord.imag] = '#'
            temp[coord.real * 2 + 1 + 1j * coord.imag] = '#'
        elif c == 'O':
            temp[coord.real * 2 + 1j * coord.imag] = '['
            temp[coord.real * 2 + 1 + 1j * coord.imag] = ']'
        elif c == '.':
            temp[coord.real * 2 + 1j * coord.imag] = '.'
            temp[coord.real * 2 + 1 + 1j * coord.imag] = '.'
        elif c == '@':
            temp[coord.real * 2 + 1j * coord.imag] = '@'
            temp[coord.real * 2 + 1 + 1j * coord.imag] = '.'
        else:
            raise RuntimeError("guard")
        coords_to_char = temp
    pos = pos.real * 2 + 1j * pos.imag
    max_coords = (max_coords[0]*2, max_coords[1])
    # start solving
    for i, d in enumerate(dir_lst):
        shift_len = 1
        while coords_to_char[pos + shift_len * d] not in ['#', '.']:
            shift_len +=1
        if coords_to_char[pos + shift_len * d] == '#':
            shift_len = 0
        else:
            if d in [W, E]:
                for shift in range(shift_len, 0, -1):
                    coords_to_char[pos + shift * d], coords_to_char[pos + (shift-1) * d] = \
                        coords_to_char[pos + (shift-1) * d], coords_to_char[pos + shift * d]
                if shift_len:
                    pos +=d
                assert coords_to_char[pos] == '@'
            else:
                if can_shift(pos, d, coords_to_char):
                    do_shift(pos, d, coords_to_char)
                    pos += d
                    assert coords_to_char[pos] == '@'
#            pos += d

        assert coords_to_char[pos] == '@'
        if debug:
            print(f"after processing dir={d}\n")
            print_maze(coords_to_char, max_coords)
            input()
    for pos_c,c  in coords_to_char.items():
        if c == '[':
            total +=  pos_c.imag* 100 + pos_c.real

    return total


parsed = parse_input(small_inp)
sol1 = part1(*parsed)
print("smallpart1:", sol1)

parsed = parse_input(big_inp)
sol1 = part1(*parsed)
print("bigpart1:", sol1)

txt_inp = get_input(15, year=2024)
parsed = parse_input(txt_inp)
sol1 = part1(*parsed)
print("sol1:", sol1)

parsed = parse_input(big_inp)
sol2 = part2(*parsed)
print("bigpart2:", sol2)
# print_maze(nodes, coords, anti)


parsed = parse_input(txt_inp)
sol2 = part2(*parsed)
print(sol2)
