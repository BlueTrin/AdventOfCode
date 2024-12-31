from aoc_lube import fetch
from collections import defaultdict

# cpy x y copies x (either an integer or the value of a register) into register y.
# inc x increases the value of register x by one.
# dec x decreases the value of register x by one.
# jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.

s = fetch(2016, 12)

reg = defaultdict(int)
instptr = 0

def cpy(x, y):
    reg[y] = reg[x] if x.isalpha() else int(x)

def inc(x):
    reg[x] += 1

def dec(x):
    reg[x] -= 1

def jnz(x, y):
    global instptr
    if (x.isalpha() and reg[x]) or (x.isnumeric() and int(x)):
        instptr += int(y) - 1

while instptr < len(s.splitlines()):
    inst = s.splitlines()[instptr]
    cmd, *args = inst.split()
    globals()[cmd](*args)
    instptr += 1

print("Part 1:", reg["a"])

reg = defaultdict(int)
instptr = 0
reg["c"] = 1
while instptr < len(s.splitlines()):
    inst = s.splitlines()[instptr]
    cmd, *args = inst.split()
    globals()[cmd](*args)
    instptr += 1

print("Part 2:", reg["a"])