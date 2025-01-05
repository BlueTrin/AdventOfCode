from aoc_lube import fetch

from intcode import Intcode
s = fetch(2019, 5)
program = list(map(int, s.split(',')))

intcode = Intcode(program.copy())
intcode.run()