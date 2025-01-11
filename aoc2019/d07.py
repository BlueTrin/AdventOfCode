from aoc_lube import fetch
from intcode import Intcode
import itertools

s = fetch(2019, 7)

program = list(map(int, s.split(',')))

max_output = 0
for phase in itertools.permutations(range(5)):
    previous_output = 0
    for comp in range(5):
        c = Intcode(program.copy())
        c.add_input(phase[comp])
        c.add_input(previous_output)
        c.run()
        previous_output = c.output.pop()
    if previous_output > max_output:
        max_output = previous_output
        combination = phase

print(f"Part 1: {max_output} {combination}")

max_output = 0
for phase in itertools.permutations(range(5, 10)):
    comps = [Intcode(program.copy()) for _ in range(5)]

    previous_output = 0
    curr_comp = 0
    for i, p in enumerate(phase):
        comps[i].add_input(p)
    while any(not c.halted for c in comps):
        c = comps[curr_comp]
        if not c.halted:
            if previous_output is not None:
                c.add_input(previous_output)
            c.run(stop_at_output=True)
            if c.halted:
                previous_output = None
            else:
                previous_output = c.output.pop()
                if curr_comp == 4:
                    fuel_signal = previous_output
        curr_comp = (curr_comp + 1) % 5

    if fuel_signal > max_output:
        max_output = fuel_signal
        combination = phase

print(f"Part 2: {max_output} {combination}")

