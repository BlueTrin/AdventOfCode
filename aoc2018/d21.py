from aoc_lube import fetch

s = fetch(2018, 21)

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

reg = [0, 0, 0, 0, 0, 0]
ipr = reg[ip]
cycle = []
while ipr < len(program):
    reg[ip] = ipr
    print(f"ip={reg[ip]} {reg} {program[reg[ip]]}")
    instr = program[reg[ip]].split()
    instr[1:] = map(int, instr[1:])
    if instr[0] == 'eqrr':
        print(f"Part1 {reg[instr[1]]}")
        break
    globals()[instr[0]](reg, instr)
    print(f"  -> {reg}")
    ipr = reg[ip]
    # print(reg)
    ipr += 1


# #ip 5
# 0: seti 123 0 3  (      123 -> [3])
# 1: bani 3 456 3  ([3] & 456 -> [3]
# 2: eqri 3 72 3   ([3] == 72?-> [3]
# 3: addr 3 5 5    ([3] + [5] -> [5]
# 4: seti 0 0 5
# 5: seti 0 9 3    (        0 -> [3])
# 6: bori 3 65536 1   [3] | 65536 -> [1]
# 7: seti 9450265 6 3   9450265->[3]
# 8: bani 1 255 4  [1] & 255 -> [4]
# 9: addr 3 4 3      [3] + [4] -> [3]
#10: bani 3 16777215 3  [3] & 16777215 -> [3]
#11: muli 3 65899 3    [3] * 65899 -> [3]
#12: bani 3 16777215 3 [3] & 16777215 -> [3]
#13: gtir 256 1 4   256 > [1] -> [4]
#14: addr 4 5 5    [4] + [5] -> [5]
#15: addi 5 1 5    [5] + 1 -> [5]
#16: seti 27 1 5   GOTO 28   27->[5]
#17: seti 0 9 4            0 -> [4]
#18: addi 4 1 2            [4] +1 -> [2]
#19: muli 2 256 2  [2] * 256 -> [2]
#20: gtrr 2 1 2     [2] > [1] -> [2]
#21: addr 2 5 5     [2] + [5] -> [5]
#22: addi 5 1 5     GOTO 24 [5]+1 -> [5]
#23: seti 25 7 5 GOTO 26 set 25 into 5
#24: addi 4 1 4      [4] +  1 -> [4]
#25: seti 17 5 5  GOTO 18 set 17 into 5
#26: setr 4 6 1      [4] -> [1]
#27: seti 7 8 5      GOTO 8    7->[5]
#28: eqrr 3 0 4      [3] == [0] -> [4]               <--- that's the line to inspect
#29:  addr 4 5 5    [4] + [5] -> [5]
#30:  seti 5 8 5    GOTO 6    5 -> [5]


def part2():
    seen = []

    r = [0] * 6

    r[3] = 123
    r[3] = r[3] & 456
    r[3] = r[3] == 72
    r[5] = r[3] + r[5]

    r[3] = 0
    r[1] = r[3] | 65536
    r[3] = 9450265

    while True:
        # 8: bani 1 255 4  [1] & 255 -> [4]
        r[4] = r[1] & 255
        r[3] = r[3] + r[4]
        r[3] = r[3] & 16777215
        r[3] = r[3] * 65899
        r[3] = r[3] & 16777215

        # 13: gtir 256 1 4   256 > [1] -> [4]
        r[4] = int(256 > r[1])
        if not r[4]:  # else goto 28
            # ip=17 [0, 65536, 0, 9532531, 0, 17] seti 0 9 4

            r[4] = r[1] // 256
            # r[4] = 0
            # while True:
            #     #18: addi 4 1 2            [4] +1 -> [2]
            #     r[2] = r[4] + 1
            #     # 19: muli 2 256 2  [2] * 256 -> [2]
            #     r[2] = r[2] * 256
            #     # 20: gtrr 2 1 2     [2] > [1] -> [2]
            #
            #     if r[2] > r[1]:
            #         break
            #     else:
            #         # ip=24 [0, 65536, 0, 9532531, 0, 24] addi 4 1 4
            #         r[4] = r[4] + 1
            #         # ip=25 [0, 65536, 0, 9532531, 1, 25] seti 17 5 5
            # ip=26 [0, 65536, 1, 9532531, 256, 26] setr 4 6 1
            r[1] = r[4]
            # ip=27 [0, 256, 1, 9532531, 256, 27] seti 7 8 5
        else:
            if r[3] not in seen:
                seen.append(r[3])
            #            print(r[3])
            else:
                break
            # ip=28 [0, 1, 1, 986758, 1, 28] eqrr 3 0 4
            if r[3] == r[0]:
                # ip=30 [0, 1, 1, 986758, 1, 30] halt
                break
            else:
                r[1] = r[3] | 65536
                r[3] = 9450265

    print("part2: "seen[-1])

part2()