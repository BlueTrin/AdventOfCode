from aoc_lube import fetch

s = fetch(2017, 16)
print(s)
programs = list('abcdefghijklmnop')

cmds = s.split(',')

def dance(programs, cmds):
    for i, cmd in enumerate(cmds):
        if cmd[0] == 's':
            n = int(cmd[1:])
            programs = programs[-n:] + programs[:-n]
        elif cmd[0] == 'x':
            a, b = map(int, cmd[1:].split('/'))
            programs[a], programs[b] = programs[b], programs[a]
        elif cmd[0] == 'p':
            a, b = cmd[1], cmd[3]
            x, y = programs.index(a), programs.index(b)
            programs[x], programs[y] = programs[y], programs[x]
    return programs

programs = dance(programs, cmds)
print(''.join(programs))

programs = list('abcdefghijklmnop')
cycle = 0
cycle_pos = {cycle: tuple(programs)}
while True:
    programs = dance(programs, cmds)
    cycle += 1
    if tuple(programs) in cycle_pos.values():
        break
    cycle_pos[cycle] = tuple(programs)

print(f"Cycle: {cycle}")
print(f"P2: {''.join(cycle_pos[1000000000% cycle])}")
# gnkaphlicmefdjbo ?
