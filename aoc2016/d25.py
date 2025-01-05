from aoc_lube import fetch
from collections import defaultdict

# cpy x y copies x (either an integer or the value of a register) into register y.
# inc x increases the value of register x by one.
# dec x decreases the value of register x by one.
# jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.

s = fetch(2016, 25)

reg = defaultdict(int)
instptr = 0

program = s.splitlines()
def cpy(x, y):
    reg[y] = reg[x] if x.isalpha() else int(x)

def inc(x):
    reg[x] += 1

def dec(x):
    reg[x] -= 1

def jnz(x, y):
    global instptr
    if (x.isalpha() and reg[x]) or (x.isnumeric() and int(x)):
        if y.isalpha():
            instptr += reg[y] - 1
        else:
            instptr += int(y) - 1

def tgl(x):
    global instptr
    try:
        inst = program[instptr + reg[x]]
    except IndexError:
        # If an attempt is made to toggle an instruction outside the program, nothing happens.
        return
    cmd, *args = inst.split()
    if len(args) == 1:
        if cmd == "inc":
            cmd = "dec"
        else:
            cmd = "inc"
    else:
        if cmd == "jnz":
            cmd = "cpy"
        else:
            cmd = "jnz"
    program[instptr + reg[x]] = f"{cmd} {' '.join(args)}"

prevbit = None
def out(x):
    global prevbit
    if x.isalpha():
        v = reg[x]
    else:
        v = int(x)

    if v not in (0, 1):
        raise StopIteration("invlaid")
    if prevbit is None:
        prevbit = v
    elif prevbit == v:
        raise StopIteration("invlaid")
    else:
        prevbit = v
#    print(v, end="")

for i in range(1, 1000):
    program = s.splitlines()
    reg = defaultdict(int)
    reg['a'] = i
    instptr = 0
    print(f"a={i}")
    prevbit = None
    try:
        while instptr < len(program):
            inst = program[instptr]
            cmd, *args = inst.split()
            globals()[cmd](*args)
            instptr += 1
    except StopIteration:
        continue

print("Part 1:", reg["a"])

# reset
program = s.splitlines()
reg = defaultdict(int)
instptr = 0
reg["a"] = 0