from importlib.util import source_hash

from aoc_lube import fetch
from intcode import Intcode


s = fetch(2019, 25)

comp = Intcode(list(map(int, s.strip().split(','))))

#                                                       HOLODECK
#                                                         |
#      ARCADE-  NAVIG      ------   HULL BREACH ------- ENGINEERING
#                |                       |                |
# (HALLWAY)   -  OBS -STORAGE         HOT CHOCO      SICL  =KITCHEN
#                 |
#                (passage
for l in '''east
take mug
north
take monolith
south
west
west
take ornament
south
east
take weather machine
west
north
west
take astrolabe
north
take fuel cell
south
south
take hologram
north
east
east
east
south
west
north
west
take bowl of rice
north
west
north'''.splitlines():
    for c in l:
        comp.add_input(ord(c))
    comp.add_input(10)


'''
mug
ornament
weather machine
astrolabe
fuel cell
monolith
hologram
bowl of rice
'''

# need ornament

while not comp.halted:
    comp.run()
    comp.trace_op7 = True
    comp.trace_op8 = False
    while comp.output:
        print(chr(comp.output.popleft()), end='')

    try:
        for c in input():
            comp.add_input(ord(c))
        comp.add_input(10)
    except EOFError:
        break
