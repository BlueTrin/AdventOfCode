from adventofcode.inputs import get_input
from adventofcode.utils import aoc_timer


def parse_input(txt_inp):
    ''' put the stub to read the code here'''
    eq_lst = []
    for r in txt_inp.split("\n"):
        if r:
            sol, rightside = r.split(":")
            sol = int(sol)
            vals = tuple(int(x) for x in rightside.split(" ") if x)
            eq_lst.append((sol, vals))
    return eq_lst


import itertools


def num_digits(n: int) -> int:
    assert n > 0
    i = int(0.30102999566398114 * (n.bit_length() - 1)) + 1
    return (10 ** i <= n) + i


def can_solve(sol, vals, part2):
    if part2:
        op_lst = [lambda x, y: x * y, lambda x, y: x + y, lambda x, y: x* pow(10,num_digits(y))+ y]
    else:
        op_lst = [lambda x,y: x*y, lambda x,y: x+y]
    for operations in itertools.product(op_lst, repeat=len(vals) - 1):
        tot =vals[0]
        for op, val_it in zip(operations, vals[1:]):
            tot = op(tot, val_it)
        if tot == sol:
            return True
    return False



def part1(eq_lst):
    total = 0
    for sol, val in eq_lst:
        if can_solve(sol, val, False):
            total += sol

    return total

def part2(eq_lst):
    total = 0
    for sol, val in eq_lst:
        if can_solve(sol, val, True):
            total += sol

    return total

if __name__ == '__main__':
    txt_inp = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''
    eq_lst = parse_input(txt_inp)
    print(part1(eq_lst))
    print(part2(eq_lst))

    txt_inp = get_input(7, year=2024)
    eq_lst = parse_input(txt_inp)
    # print(part1(eq_lst))
    print(part2(eq_lst))

