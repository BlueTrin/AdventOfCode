import copy
import colorama
import blessings
from doctest import debug

from utils2018.aoc_input import get_input
from utils2018 import aoc_timer, parse_complex
from typing import Dict, List, Tuple, Set
import math
import itertools
import networkx as nx
import scipy
import numpy as np
import sys
import logging
thismodule = sys.modules[__name__]
logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
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


 #   _____ ____  _____  ______   _    _ ______ _____  ______
 #  / ____/ __ \|  __ \|  ____| | |  | |  ____|  __ \|  ____|
 # | |   | |  | | |  | | |__    | |__| | |__  | |__) | |__
 # | |   | |  | | |  | |  __|   |  __  |  __| |  _  /|  __|
 # | |___| |__| | |__| | |____  | |  | | |____| | \ \| |____
 #  \_____\____/|_____/|______| |_|  |_|______|_|  \_\______|
 #
class CPU:
    def __init__(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.instptr = 0
        self.output = []
    def __repr__(self):
        return f"CPU(A={self.A}, B={self.B}, C={self.C}, instptr={self.instptr}, output={self.output})"

def combo(l, cpu: CPU):
    if l <= 3:
        return l
    elif l == 4:
        return cpu.A
    elif l == 5:
        return cpu.B
    elif l == 6:
        return cpu.C


def op_0(l, cpu):
    cpu.A = cpu.A // 2**combo(l, cpu)

def op_1(l, cpu):
    cpu.B = cpu.B ^ l

def op_2(l, cpu):
    cpu.B = combo(l, cpu) % 8

def op_3(l, cpu):
    if cpu.A != 0:
        cpu.instptr = l-2

def op_4(l, cpu):
    cpu.B = cpu.B ^ cpu.C

def op_5(l, cpu):
    cpu.output.append(combo(l, cpu) % 8)

def op_6(l, cpu):
    cpu.B = cpu.A // 2**combo(l, cpu)

def op_7(l, cpu):
    cpu.C = cpu.A // 2**combo(l, cpu)

op_map = {}
for i in range(8):
    op_map[i] = getattr(thismodule, f'op_{i}')

def read_program(inp):
    register_txt, program_txt = inp.split("\n\n")
    cpu = CPU()
    cpu.A, cpu.B, cpu.C = [int(l.split(":")[1]) for l in register_txt.splitlines() ]
    program = [int(x) for x in program_txt.split(":")[1].split(",")]
    return cpu, program

def part1(inp,debug=False):

    cpu, program = read_program(inp)

    while cpu.instptr+1 < len(program):
        op, l = program[cpu.instptr:cpu.instptr+2]
        old = copy.deepcopy(cpu)
        op_map[op](l, cpu)
        cpu.instptr += 2
        if debug:
            logger.info(
                f"A={old.A}->{cpu.A}, B={old.B}->{cpu.B}, C={old.C}->{cpu.C}, INSTPTR={old.instptr}->{cpu.instptr} - OP={op} l={l}")
    return ','.join([str(x) for x in cpu.output])

def run_program(orig_cpu, program, A, debug=False):
    cpu = copy.deepcopy(orig_cpu)
    cpu.A = A
    cpu.instptr = 0
    while cpu.instptr+1 < len(program):
        op, l = program[cpu.instptr:cpu.instptr+2]
        old = copy.deepcopy(cpu)
        op_map[op](l, cpu)
        cpu.instptr += 2
        if debug:
            logger.info(
                f"A={old.A}->{cpu.A}, B={old.B}->{cpu.B}, C={old.C}->{cpu.C}, INSTPTR={old.instptr}->{cpu.instptr} - OP={op} l={l}")
    return cpu.output

def try_rec(cpu, program, a):
    cpu.A = a
    res = run_program(cpu, program, a )
    if res == program:
        return a
    elif len(res) >= len(program):
        return None
    elif program[-len(res):]  == res:
        for i in range(0, 8):
            rec = try_rec(cpu, program, i  + (a<<3))
            if rec is not None:
                return res




def part2(inp):
    cpu, program = read_program(inp)

    for a in range(8):
        res = try_rec(cpu, program, a)
        if res is not None:
            return res
    return


i1 = '''Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
'''

sol1 = part1(i1, True)
print(sol1)

ii = '''Register A: 33940147
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,1,6,4,2,5,5,0,3,3,0'''
sol1 = part1(ii, debug=True)
print(sol1)
#
# sol2 = part2(i1)
# print(sol2)
# # print_maze(nodes, coords, anti)

sol2 = part2(ii)
print(sol2)
