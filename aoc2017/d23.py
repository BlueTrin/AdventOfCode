from aoc_lube import fetch
from collections import defaultdict, deque

s = fetch(2017, 23)

class Program(object):
    def __init__(self, program, pid):
        self.reg = {c: 0 for c in 'abcdefgh'}
        self.reg['p'] = pid
        self.program = program
        self.ip = 0
        self.send_queue = deque()
        self.send_count = 0
        self.rec_queue = deque()
        self.waiting = False
        self.halted = False
        self.mul_count = 0
        self.debug = False

    def run(self):
        while 0 <= self.ip < len(self.program):
            self.waiting = False
            r = self.program[self.ip]
            cmd, *args = r.split()

            if self.debug:
                print(f"{self.ip}: {r} {self.reg}")

            if len(args) >= 2:
                args[1] = int(args[1]) if args[1].lstrip('-').isdigit() else self.reg.get(args[1])

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
            elif cmd == 'sub':
                assert not args[0].isdigit()
                self.reg[args[0]] -= args[1]
            elif cmd == 'mul':
                self.mul_count += 1
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
            elif cmd == 'jnz':
                if args[0].strip('-').isdigit():
                    val = int(args[0])
                else:
                    val = self.reg.get(args[0])

                if val != 0:
                    self.ip += args[1]
                    continue
            elif cmd == 'jgz':
                if args[0].strip('-').isdigit():
                    val = int(args[0])
                else:
                    val = self.reg.get(args[0])

                if val > 0:
                    self.ip += args[1]
                    continue
            self.ip += 1
        self.halted = True

p = Program(s.splitlines(), 0)
p.run()
print(f"Part1: {p.mul_count}")
assert p.mul_count == 9409

from utils import primes

a=b=c=d=e=f=g=h=0
a=1
#b = 109900
c = 126900

prime_lst = primes(126901)
# CODE IS ACTUALLY COUNTING THE NON PRIMES BETWEEN 109900 AND 126900
for b in range(109900, c+1, 17):
    if b not in prime_lst: # 24
        h += 1

print(f"Part2: {h}")

# p = Program(s.splitlines(), 0)
# p.reg['a'] = 1
# p.debug = True
# p.run()

'''
0: set b 99
1: set c b
  -> c = b = 99

2: jnz a 2
3: jnz 1 5
4: mul b 100
5: sub b -100000
6: set c b
7: sub c -17000

 -> if a !=0:
      b *= 100
      b -= -100000
      c = b
      c -= -17000
        

8: set f 1
9: set d 2
10: set e 2

 -> f = 1
    d = 2
    e = 2

11: set g d
12: mul g e
13: sub g b
14: jnz g 2
15: set f 0
16: sub e -1
17: set g e
18: sub g b
19: jnz g -8

while True
    g = d * e - b
    if g == 0:
        f = 0
    e -= 1
    g = e
    g -= b
    if g == 0:
        break
        

20: sub d -1
21: set g d
22: sub g b
23: jnz g -13
24: jnz f 2
25: sub h -1
26: set g b
27: sub g c
28: jnz g 2
29: jnz 1 3 -> EXIT
30: sub b -17
31: jnz 1 -23
'''