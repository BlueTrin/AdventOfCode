from adventofcode.inputs import get_input
from adventofcode.utils import aoc_timer

 #   _____ ______ _   _ ______ _____            _
 #  / ____|  ____| \ | |  ____|  __ \     /\   | |
 # | |  __| |__  |  \| | |__  | |__) |   /  \  | |
 # | | |_ |  __| | . ` |  __| |  _  /   / /\ \ | |
 # | |__| | |____| |\  | |____| | \ \  / ____ \| |____
 #  \_____|______|_| \_|______|_|  \_\/_/    \_\______|
 #
import itertools

N = -1j
S = 1j
W = -1
E = 1

 #  _____  ______          _____    _____ _   _ _____  _    _ _______
 # |  __ \|  ____|   /\   |  __ \  |_   _| \ | |  __ \| |  | |__   __|
 # | |__) | |__     /  \  | |  | |   | | |  \| | |__) | |  | |  | |
 # |  _  /|  __|   / /\ \ | |  | |   | | | . ` |  ___/| |  | |  | |
 # | | \ \| |____ / ____ \| |__| |  _| |_| |\  | |    | |__| |  | |
 # |_|  \_\______/_/    \_\_____/  |_____|_| \_|_|     \____/   |_|


def parse_input(txt_inp):
    ''' put the stub to read the code here'''
    inp = []

    nodes = {}
    maybe = set()
    for i_y, r in enumerate(txt_inp.split("\n")):
        if r:
            for i_x, c in enumerate(r):
                # if c == ".":
                maybe.add(i_x + i_y * 1j)
                if c != ".":
                    if c not in nodes:
                        nodes[c] = set()

                    nodes[c].add(i_x + i_y *1j)

    coords = (len(txt_inp.split("\n"))-1) * 1j + len(txt_inp.split("\n")[0])
    return nodes, coords, maybe


 #   _____ ____  _____  ______   _    _ ______ _____  ______
 #  / ____/ __ \|  __ \|  ____| | |  | |  ____|  __ \|  ____|
 # | |   | |  | | |  | | |__    | |__| | |__  | |__) | |__
 # | |   | |  | | |  | |  __|   |  __  |  __| |  _  /|  __|
 # | |___| |__| | |__| | |____  | |  | | |____| | \ \| |____
 #  \_____\____/|_____/|______| |_|  |_|______|_|  \_\______|
 #

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



def part1(nodes, coords, maybe):
    anti = set()
    for p in maybe:
        is_antinode = False
        for freq, freq_coords in nodes.items():
            dst_set = set()
            for n in freq_coords:
                if (n-p) * 2 in dst_set or (n-p) / 2 in dst_set:
                    anti.add(p)
                    is_antinode = True
                    break
                else:
                    dst_set.add(n-p)
            if is_antinode:
                break

    return len(anti), anti

import math

def part2(nodes, max_coords, maybe):
    anti = set()
    for freq, c_coords in nodes.items():
        if len(c_coords) >= 2:
            for c in c_coords:
                anti.add(c)

        for x1, x2 in itertools.combinations(c_coords, 2):
            total_dst = x2-x1

            gcd = math.gcd(int(total_dst.real), int(total_dst.imag))
            dst_inc = total_dst / gcd
            for i in range(-1000, 1000):    # can't be bothered lol
                pt = x1 + i *dst_inc
                if pt in maybe:
                    anti.add(x1 + i *dst_inc)


    return len(anti), anti


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
    nodes, coords, maybe = parse_input(txt_inp)
    sol1, anti = part1(nodes, coords, maybe)
    print(sol1)
    # print_maze(nodes, coords, anti)
    sol2, anti = part2(nodes, coords, maybe)
    print(sol2)
    # print_maze(nodes, coords, anti)

    txt_inp = get_input(8, year=2024)
    nodes, coords, maybe = parse_input(txt_inp)
    sol1, anti = part1(nodes, coords, maybe)
    print(sol1)
    # print_maze(nodes, coords, anti)
    sol2, anti = part2(nodes, coords, maybe)
    print(sol2)
