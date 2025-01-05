from aoc_lube import fetch

s = fetch(2018, 16)

tst_cases = []
samples = s.split('\n\n\n\n')[0].split('\n\n')
for sample_s in samples:
    bef_s, instr_s, aft_s = sample_s.splitlines()
    bef = list(map(int, bef_s[9:-1].split(', ')))
    instr = list(map(int, instr_s.split()))
    aft = list(map(int, aft_s[9:-1].split(', ')))
    tst_cases.append((bef, instr, aft))


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

opcodes = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

def test_case(tst_case):
    bef, instr, aft = tst_case
    valid_opcodes = 0
    for opcode in opcodes:
        reg = opcode(bef.copy(), instr)
        if reg == aft:
            valid_opcodes += 1
    return valid_opcodes


print("Part 1:", sum(test_case(tst_case) >= 3 for tst_case in tst_cases))

# Part 2:
opcode_map = {}
for tst_case in tst_cases:
    bef, instr, aft = tst_case
    valid_opcodes = []
    for opcode in opcodes:
        reg = opcode(bef.copy(), instr)
        if reg == aft:
            valid_opcodes.append(opcode)
    if instr[0] in opcode_map:
        opcode_map[instr[0]] &= set(valid_opcodes)
    else:
        opcode_map[instr[0]] = set(valid_opcodes)

while True:
    for k, v in opcode_map.items():
        if len(v) == 1:
            for k2, v2 in opcode_map.items():
                if k != k2:
                    opcode_map[k2] -= v
    if all(len(v) == 1 for v in opcode_map.values()):
        break
print(opcode_map)

prg = [[int(x) for x in r.split()]for r in s.split('\n\n\n\n')[1].splitlines() ]


reg = [0] *4
opcode_map = {k: list(v)[0] for k, v in opcode_map.items()}
for instr in prg:
    opcode_map[instr[0]](reg, instr)

print(reg[0])
