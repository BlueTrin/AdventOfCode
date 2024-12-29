from aoc_lube import fetch

s = fetch(2015, 23)
a = 0
b = 0
ptr = 0

def ev(var):
    if isinstance(var, int):
        return var
    else:
        return globals()[var]


def hlf(var):
    """
    hlf r sets register r to half its current value, then continues with the next instruction.
    """
    globals()[var] //= 2


def tpl(var):
    """
    tpl r sets register r to triple its current value, then continues with the next instruction.
    """
    globals()[var] *= 3

def inc(var):
    """
    inc r increments register r, adding 1 to it, then continues with the next instruction.
    """
    globals()[var] += 1


def jmp(val):
    """
    jmp offset is a jump; it continues with the instruction offset away relative to itself.
    """
    global ptr
    ptr += val -1


def jie(var, val):
    """
    jie r, offset is like jmp, but only jumps if register r is even ("jump if even").
    """
    global ptr
    if ev(var) % 2 == 0:
        ptr += val -1

def jio(var, val):
    """
    jio r, offset is like jmp, but only jumps if register r is 1 ("jump if one", not odd).
    """
    global ptr
    if ev(var) == 1:
        ptr += val -1

program = [x for x in s.splitlines() if x]

while ptr < len(program):
    instr = program[ptr]
    cmd, args  = instr.split(' ', 1)
    oldptr, olda, oldb = ptr, a, b
    globals()[cmd](*[ x if x in ['a', 'b'] else int(x) for x in args.split(', ')])
    ptr += 1
#    print(f"{oldptr} {instr} {oldptr}->{ptr} {olda}->{a} {oldb}->{b}")

print(f"part1: {b}")
a = 1
b = 0
ptr = 0
while ptr < len(program):
    instr = program[ptr]
    cmd, args  = instr.split(' ', 1)
    oldptr, olda, oldb = ptr, a, b
    globals()[cmd](*[ x if x in ['a', 'b'] else int(x) for x in args.split(', ')])
    ptr += 1
#    print(f"{oldptr} {instr} {oldptr}->{ptr} {olda}->{a} {oldb}->{b}")

print(f"part2: {b}")