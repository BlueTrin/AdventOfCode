from aoc_lube import fetch

s = fetch(2019, 1)

def fuel(mass, part2=False):
    '''
    Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module,
     take its mass, divide by three, round down, and subtract 2.
    '''
    if part2:
        total = 0
        while mass > 0:
            mass = mass // 3 - 2
            if mass > 0:
                total += mass
        return total
    else:
        return mass // 3 - 2

total = 0
for r in s.splitlines():
    total += fuel(int(r))
print(total)

total = 0
for r in s.splitlines():
    total += fuel(int(r), part2=True)
print(total)
