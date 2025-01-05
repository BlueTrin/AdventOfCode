
from aoc_lube import fetch
s = fetch(2018, 19)
# s = '''#ip 0
# seti 5 0 1
# seti 6 0 2
# addi 0 1 0
# addr 1 2 3
# setr 1 0 0
# seti 8 0 4
# seti 9 0 5'''
def addr(reg, instr):
    # addr (add register) stores into register C the result of adding register A and register B.
    reg[instr[3]] = reg[instr[1]] + reg[instr[2]]
    return reg

def addi(reg, instr):
    # addi (add immediate) stores into register C the result of adding register A and value B.
    reg[instr[3]] = reg[instr[1]] + instr[2]
    return reg

def mulr(reg, instr):
    # mulr (multiply register) stores into register C the result of multiplying register A and register B.
    reg[instr[3]] = reg[instr[1]] * reg[instr[2]]
    return reg

def muli(reg, instr):
    # muli (multiply immediate) stores into register C the result of multiplying register A and value B.
    reg[instr[3]] = reg[instr[1]] * instr[2]
    return reg

def banr(reg, instr):
    # banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
    reg[instr[3]] = reg[instr[1]] & reg[instr[2]]
    return reg

def bani(reg, instr):
    # bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
    reg[instr[3]] = reg[instr[1]] & instr[2]
    return reg

def borr(reg, instr):
    # borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
    reg[instr[3]] = reg[instr[1]] | reg[instr[2]]
    return reg

def bori(reg, instr):
    # bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
    reg[instr[3]] = reg[instr[1]] | instr[2]
    return reg

def setr(reg, instr):
    # setr (set register) copies the contents of register A into register C. (Input B is ignored.)
    reg[instr[3]] = reg[instr[1]]
    return reg

def seti(reg, instr):
    # seti (set immediate) stores value A into register C. (Input B is ignored.)
    reg[instr[3]] = instr[1]
    return reg

def gtir(reg, instr):
    # gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
    reg[instr[3]] = 1 if instr[1] > reg[instr[2]] else 0
    return reg

def gtri(reg, instr):
    # gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
    reg[instr[3]] = 1 if reg[instr[1]] > instr[2] else 0
    return reg

def gtrr(reg, instr):
    # gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
    reg[instr[3]] = 1 if reg[instr[1]] > reg[instr[2]] else 0
    return reg

def eqir(reg, instr):
    # eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
    reg[instr[3]] = 1 if instr[1] == reg[instr[2]] else 0
    return reg

def eqri(reg, instr):
    # eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
    reg[instr[3]] = 1 if reg[instr[1]] == instr[2] else 0
    return reg

def eqrr(reg, instr):
    # eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
    reg[instr[3]] = 1 if reg[instr[1]] == reg[instr[2]] else 0
    return reg

ip = int(s.splitlines()[0].split()[1])
program = s.splitlines()[1:]
print(ip, program)

reg = [1, 0, 0, 0, 0, 0]
ipr = reg[ip]
while ipr < len(program):
    reg[ip] = ipr
    # print(f"ip={reg[ip]} {reg} {program[reg[ip]]}")
    instr = program[reg[ip]].split()
    instr[1:] = map(int, instr[1:])
    globals()[instr[0]](reg, instr)
    ipr = reg[ip]
    ipr += 1


print(f"ip={reg[ip]} {reg}")
# 255 too low 257 too low
