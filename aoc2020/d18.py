from aoc_lube import fetch
import re
from operator import add, mul

s = fetch(2020, 18)
print(s)

def find_next_par(expr, start):
    par_count = 1
    for i, c in enumerate(expr[start:]):
        if c == '(':
            par_count += 1
        elif c == ')':
            par_count -= 1
        if par_count == 0:
            return i+start
    return -1

def get_val(expr, i):
    if expr[i].isdigit():
        return int(expr[i]), i+1
    elif expr[i] == '(':
        next_par = find_next_par(expr, i+1)
        return eval_expr(expr[i+1:next_par]), next_par+1
    else:
        return None, i+1

def eval_expr(expr):
    expr = expr.replace(' ', '')

    val, icur = get_val(expr, 0)
    expr = expr[icur:]
    while expr:
        if expr[0] == '+':
            op = add
        elif expr[0] == '*':
            op = mul
        else:
            raise ValueError(f"Unknown operator {expr}")

        val2, icur = get_val(expr, 1)
        val = op(val, val2)
        expr = expr[icur:]

    return val

assert eval_expr('1 + 2 * 3 + 4 * 5 + 6') == 71
assert eval_expr('2 * 3 + (4 * 5)') == 26
assert eval_expr('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert eval_expr('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert eval_expr('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632
print(f"Part1: {sum(eval_expr(r) for r in s.splitlines())}")

def eval_expr2(expr):
    tokens = []
    expr = expr.replace(' ', '')
    while expr:
        if expr[0].isdigit():
            tokens.append(int(expr[0]))
            expr = expr[1:]
        elif expr[0] == '(':
            next_par = find_next_par(expr, 1)
            tokens.append(eval_expr2(expr[1:next_par]))
            expr = expr[next_par+1:]
        elif expr[0] in '+*':
            tokens.append(expr[0])
            expr = expr[1:]
        else:
            raise ValueError(f"Unknown token {expr}")

    while '+' in tokens:
        i = tokens.index('+')
        tokens[i-1] = tokens[i-1] + tokens[i+1]
        tokens.pop(i)
        tokens.pop(i)

    while '*' in tokens:
        i = tokens.index('*')
        tokens[i-1] = tokens[i-1] * tokens[i+1]
        tokens.pop(i)
        tokens.pop(i)

    assert len(tokens) == 1
    return tokens[0]


assert eval_expr2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340

print(f"Part2: {sum(eval_expr2(r) for r in s.splitlines())}")
