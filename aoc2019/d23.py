from aoc_lube import fetch
from intcode import Intcode


s = fetch(2019, 23)
nat = None
comp_lst = [Intcode(list(map(int, s.strip().split(',')))) for _ in range(50)]
for i, comp in enumerate(comp_lst):
    comp.add_input(i)

not_all_halted = True
part1 = None
eeen = set()
while not_all_halted:
    not_all_halted = False
    for i, comp in enumerate(comp_lst):
        if comp.halted:
            continue

        not_all_halted = True
        comp.run()
        while comp.output:
            dest, x, y = comp.output.popleft(), comp.output.popleft(), comp.output.popleft()
            if dest == 255:
                if part1 is None:
                    part1 = y
                    print(f"Part1: y={y}")
                nat = (x, y)
            else:
                comp_lst[dest].add_input(x)
                comp_lst[dest].add_input(y)

    if all(not comp.input for comp in comp_lst) and nat:
        if nat[1] in eeen:
            print(f"Part2: {nat[1]}")
            break
        eeen.add(nat[1])
        comp_lst[0].add_input(nat[0])
        comp_lst[0].add_input(nat[1])

    for comp in comp_lst:
        if comp.input_needed and not comp.input:
            comp.add_input(-1)

pass