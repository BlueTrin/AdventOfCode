from aoc_lube import fetch
import logging


logging.basicConfig(level=logging.DEBUG)
s = fetch(2025, 10)

part1 = None

ret = 0
coords = []

row_lst = []
for line in s.splitlines():
    lights_str, *wiring_str_lst, joltage_str = line.strip().split(' ')
    lights = tuple([c == '#' for c in lights_str[1:-1]])

    wiring_lst = []
    for wiring_str in wiring_str_lst:
        wiring = [False] * len(lights)
        for lightid in tuple(map(int,  wiring_str[1:-1].split(','))):
            wiring[lightid] = True
        wiring_lst.append(tuple(wiring))

    joltage = tuple(eval('[' + joltage_str[1:-1] + ']'))

    row_lst.append( (lights, wiring_lst, joltage) )


def solve_part1_row(light, wiring_lst):
    ret = 0
    curr_step = []
    curr_step.append( (False,)*len(light) )
    seen = set()
    seen.add( curr_step[0] )

    while True:
        next_step = []
        for state in curr_step:
            for wiring in wiring_lst:
                res = tuple(a ^ b for a, b in zip(state, wiring))
                if res == light:
                    return ret + 1
                if res in seen:
                    continue
                seen.add(res)
                next_step.append(res)
        curr_step = next_step
        ret += 1
        if len(curr_step) == 0:
            raise ValueError("No solution found")


part1 = 0
for i, (light, wiring_lst, _joltage) in enumerate(row_lst):
    part1 += solve_part1_row(light, wiring_lst)
print(f"part 1: {part1}")

part2 = 0
from z3 import *
for i, (_light, wiring_lst, joltage) in enumerate(row_lst):
    opt = Optimize()
    z3vars = [Int(f'x{i}') for i in range(len(wiring_lst))]
    for j, jolt in enumerate(joltage):
        opt.add(sum([z3vars[i] for i, wiring in enumerate(wiring_lst) if wiring[j]]) == jolt)

    cost = Int('cost')

    for i in range(len(wiring_lst)):
        opt.add(z3vars[i] >= 0)

    opt.add(cost == sum(z3vars))
    h = opt.minimize(cost)
    # print(opt.check())
    # print(opt.lower(h))
    # print(opt.model())
    if opt.check() == sat:
        part2 += opt.lower(h).as_long()
print(f"part 2: {part2}")