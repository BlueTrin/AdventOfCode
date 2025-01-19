from aoc_lube import fetch
from collections import defaultdict, deque

s = fetch(2017, 18)

class Program(object):
    def __init__(self, program, pid):
        self.reg = defaultdict(int)
        self.reg['p'] = pid
        self.program = program
        self.ip = 0
        self.send_queue = deque()
        self.send_count = 0
        self.rec_queue = deque()
        self.waiting = False
        self.halted = False

    def run(self):
        while 0 <= self.ip < len(self.program):
            self.waiting = False
            r = self.program[self.ip]
            cmd, *args = r.split()
            if len(args) >= 2:
                args[1] = int(args[1]) if args[1].lstrip('-').isdigit() else self.reg[args[1]]

            if cmd == 'snd':
                assert not args[0].isdigit()
                self.send_count += 1
                self.send_queue.append(self.reg[args[0]])
            elif cmd == 'set':
                assert not args[0].isdigit()
                self.reg[args[0]] = args[1]
            elif cmd == 'add':
                assert not args[0].isdigit()
                self.reg[args[0]] += args[1]
            elif cmd == 'mul':
                assert not args[0].isdigit()
                self.reg[args[0]] *= args[1]
            elif cmd == 'mod':
                assert not args[0].isdigit()
                self.reg[args[0]] %= args[1]
            elif cmd == 'rcv':
                assert not args[0].isdigit()
                if self.rec_queue:
                    self.reg[args[0]] = self.rec_queue.popleft()
                else:
                    self.waiting = True
                    return
            elif cmd == 'jgz':
                if args[0].strip('-').isdigit():
                    val = int(args[0])
                else:
                    val = self.reg[args[0]]

                if val > 0:
                    self.ip += args[1]
                    continue
            self.ip += 1
        self.halted = True

p1 = Program(s.splitlines(), 0)
p1.run()
print(f"Part1: {p1.send_queue[-1]}")
assert p1.send_queue[-1] == 8600

# s = '''snd 1
# snd 2
# snd p
# rcv a
# rcv b
# rcv c
# rcv d'''
p0 = Program(s.splitlines(), 0)
p1 = Program(s.splitlines(), 1)

while (not p0.halted or not p1.halted) and not (p0.waiting and p1.waiting):
    p0.run()
    if p0.send_queue:
        p1.waiting = False
    p1.rec_queue.extend(p0.send_queue)
    p0.send_queue.clear()

    p1.run()
    if p1.send_queue:
        p0.waiting = False
    p0.rec_queue.extend(p1.send_queue)
    p1.send_queue.clear()

print(f"Part2: {p1.send_count}")
#
# debug = True
# part1 = None
# program = s.splitlines()
#
# while 0 <= reg['ip'] < len(program):
#     r = program[reg['ip']]
#     cmd, *args = r.split()
#     if len(args) >= 2:
#         args[1] = int(args[1]) if args[1].lstrip('-').isdigit() else reg[args[1]]
#
#     if cmd == 'snd':
#         if debug:
#             print(f"{r} - Playing sound: {reg[args[0]]}")
#         reg['snd'] = reg[args[0]]
#     elif cmd == 'set':
#         reg[args[0]] = args[1]
#         if debug:
#             print(f"{r} - Setting {args[0]} to {args[1]}")
#     elif cmd == 'add':
#         reg[args[0]] += args[1]
#         if debug:
#             print(f"{r} - Adding {args[1]} to {args[0]} = {reg[args[0]]}")
#     elif cmd == 'mul':
#         reg[args[0]] *= args[1]
#         if debug:
#             print(f"{r} - Multiplying {args[1]} to {args[0]} = {reg[args[0]]}")
#     elif cmd == 'mod':
#         reg[args[0]] %= args[1]
#         if debug:
#             print(f"{r} - Modulo {args[1]} to {args[0]} = {reg[args[0]]}")
#     elif cmd == 'rcv':
#         if reg[args[0]] != 0:
#             if part1 is None:
#                 part1 = reg['snd']
#                 print(f"Part1: {part1}")
#             break
#     elif cmd == 'jgz':
#         if reg[args[0]] > 0:
#             reg['ip'] += args[1]
#             if debug:
#                 print(f"{r} - Jumping to {reg['ip']}")
#             continue
#     reg['ip'] += 1

