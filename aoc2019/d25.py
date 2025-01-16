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
- bowl of rice (8192)
- monolith (64)
- mug (32768)
- weather machine (1)
- fuel cell (4)
- astrolabe (1073741824)
- ornament (131072)
- hologram (2048)

Correct was astrolabe + ornament + HOLOGRAM 
'''

# nothing = heavier
# monolith + weather = heavier

# LIGHTER
# - monolith
# - weather machine
# - astrolabe
# - ornament
# - hologram

# HEAVIER
# - weather machine
# - astrolabe
# - ornament
# - hologram

while not comp.halted:
    comp.run()
    comp.set_watch(2772)
    while comp.output:
        print(chr(comp.output.popleft()), end='')

    try:
        for c in input():
            comp.add_input(ord(c))
        comp.add_input(10)
    except EOFError:
        break
