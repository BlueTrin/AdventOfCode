from aoc_lube import fetch
from collections import defaultdict

s = fetch(2017, 8)

reg_lst = defaultdict(int)
max_val = 0

def apply_op(reg, op, val):
    if op == 'inc':
        reg_lst[reg] += int(val)
    elif op == 'dec':
        reg_lst[reg] -= int(val)

def cond_met(reg, op, val):
    if op == '==':
        return reg_lst[reg] == int(val)
    elif op == '!=':
        return reg_lst[reg] != int(val)
    elif op == '>':
        return reg_lst[reg] > int(val)
    elif op == '<':
        return reg_lst[reg] < int(val)
    elif op == '>=':
        return reg_lst[reg] >= int(val)
    elif op == '<=':
        return reg_lst[reg] <= int(val)
    else:
        raise ValueError(f"Unknown operator: {op}")

def execute(s):
    global max_val
    for r in s.splitlines():
        instr, cond = r.split(' if ')
        reg, op, val = instr.split()
        cond_reg, cond_op, cond_val = cond.split()

        if cond_met(cond_reg, cond_op, cond_val):
            apply_op(reg, op, val)
            max_val = max(max_val, reg_lst[reg])

execute(s)
print(f"Part1: {max(reg_lst.values())}")
print(f"Part2: {max_val}")