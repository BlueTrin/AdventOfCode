from aoc_lube import fetch
import itertools

s = fetch(2020, 14)

print(s)

mem = {}

for r in s.splitlines():
    if r.startswith('mask'):
        mask = r.split()[-1]
        # all digits values are to be added
        mask_add = int(mask.replace('X', '0'), 2)
        # apply or on all the X digits
        mask_or = int(mask.replace('1', '0').replace('X', '1'), 2)
    elif r.startswith('mem'):
        addr, val = map(int, r.replace('mem[', '').replace(']', '').split(' = '))
        mem[addr] = (val & mask_or) | mask_add
    else:
        raise ValueError(f"Unknown instruction: {r}")

print(f"Part1: {sum(mem.values())}")

# s = '''mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1'''
debug = False

mem = {}
for r in s.splitlines():
    if r.startswith('mask'):
        mask = r.split()[-1]
        # If the bitmask bit is 0, the corresponding memory address bit is unchanged.
        pass # do nothing ofr this case

        # If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
        mask_or = int(mask.replace('X', '0'), 2)

        # If the bitmask bit is X, the corresponding memory address bit is floating.
        mask_and = int(mask.replace('0', '1').replace('X', '0'), 2)   # null the bytes before doing product combinations
        float_pos = [i for i, c in enumerate(mask[::-1]) if c == 'X']

    elif r.startswith('mem'):
        addr, val = map(int, r.replace('mem[', '').replace(']', '').split(' = '))
        base_addr = (addr & mask_and) | mask_or
        for comb in itertools.product([0, 1], repeat=len(float_pos)):
            addr = base_addr
            for i, c in enumerate(comb):
                addr |= (c << float_pos[i])
            mem[addr] = val
            if debug:
                print(f"mem[{addr}] = {val}")
    else:
        raise ValueError(f"Unknown instruction: {r}")

print(f"Part2: {sum(mem.values())}")
# 654588463920 too low