from aoc_lube import fetch
import itertools

s = fetch(2019, 2)

def opcode1(p, a, b, c):
    '''
    Opcode 1 adds together numbers read from two positions and stores the result in a third position.
    The three integers immediately after the opcode tell you these three positions -
     the first two indicate the positions from which you should read the input values, and the
     third indicates the position at which the output should be stored.
    '''
    p[c] = p[a] + p[b]
    return p

def opcode2(p, a, b, c):
    '''
    Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
    Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.
    '''
    p[c] = p[a] * p[b]
    return p

program = list(map(int, s.split(',')))
program[1] = 12
program[2] = 2

ptr = 0
while program[ptr] != 99:
    opcode, a, b, c = program[ptr:ptr+4]
    if opcode == 1:
        program = opcode1(program, a, b, c)
    elif opcode == 2:
        program = opcode2(program, a, b, c)
    ptr += 4

print(f"Part 1: {program[0]}")

for p1, p2 in itertools.product(range(100), repeat=2):
    program = list(map(int, s.split(',')))
    program[1] = p1
    program[2] = p2

    ptr = 0
    while program[ptr] != 99:
        opcode, a, b, c = program[ptr:ptr+4]
        if opcode == 1:
            program = opcode1(program, a, b, c)
        elif opcode == 2:
            program = opcode2(program, a, b, c)
        ptr += 4

    if program[0] == 19690720:
        print(f"Part 2: {100 * p1 + p2}")
        break