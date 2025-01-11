from aoc_lube import fetch
from intcode import Intcode
from utils.utils import Point


s = fetch(2019, 17)

prog = list(map(int, s.strip().split(',')))

z = Intcode(prog)
z.run()
print(z.output)
maze = ''.join(map(chr, z.output))
z.output.clear()
print(maze)
#
# maze = '''..#..........
# ..#..........
# #######...###
# #.#...#...#.#
# #############
# ..#...#...#..
# ..#####...^..'''

m = {}
for iy, r in enumerate(maze.split('\n')):
    for ix, c in enumerate(r):
        m[Point(ix, iy)] = c

total = 0
for p, c in m.items():
    if c == '#':
        if sum([m.get(adj) == '#' for adj in p.adjacent4()]) > 2:
            # print(p)
            total += p.x * p.y

print(f"Part 1: {total}")

z = Intcode(prog)
z.p[0] = 2
for ch in 'A,B,A,C,B,A,C,B,A,C\n':
    z.add_input(ord(ch))

for ch in "L,6,L,4,R,12\n":
    z.add_input(ord(ch))

for ch in "L,6,R,12,R,12,L,8\n":
    z.add_input(ord(ch))

for ch in "L,6,L,10,L,10,L,6\n":
    z.add_input(ord(ch))

z.add_input(ord('n'))
z.add_input(ord('\n'))

z.run()

if not z.halted:
    print("not halted")
print(''.join(map(chr, z.output)))
print(f"Part2: {z.output[-1]}")
#A B A C B A C B A C


# A = L,6,L,4 R 12
# B = L6  R 12 R 12 L 8
# A = L6 L4 R12
# C = L6 L10 L 10 L6
# B = L6 r12 r12 l8
# A l6 l4 r 12
# C = l6 l10 l10 l6
# B l6  r12 r12 l8
# A l6 l4 r12
# C l6  l10 l10 l6