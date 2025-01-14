from aoc_lube import fetch
from intcode import Intcode


s = fetch(2019, 21)

prog = list(map(int, s.strip().split(',')))

comp = Intcode(prog)
comp.run()
print(''.join(map(chr, [comp.output.popleft() for x in range(len(comp.output))])))

springscript = '''NOT A J
NOT B T
OR T J
NOT C T
OR T J
AND D J'''

for line in springscript.splitlines():
    for c in line:
        comp.add_input(ord(c))
    comp.add_input(10)

for c in 'WALK':
    comp.add_input(ord(c))

comp.add_input(10)
comp.run()
while comp.output:
    c = comp.output.popleft()
    if c < 256:
        print(chr(c), end='')
    else:
        print(c)


# part 2
comp = Intcode(prog)
comp.run()
print(''.join(map(chr, [comp.output.popleft() for x in range(len(comp.output))])))

springscript = '''
NOT B T
OR T J
NOT C T
OR T J
AND D J
AND H J
NOT A T
OR T J
'''

for line in springscript.splitlines():
    if not line:
        continue
    for c in line:
        comp.add_input(ord(c))
    comp.add_input(10)

for c in 'RUN':
    comp.add_input(ord(c))

comp.add_input(10)
comp.run()
while comp.output:
    c = comp.output.popleft()
    if c < 256:
        print(chr(c), end='')
    else:
        print(c)

