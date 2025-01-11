from aoc_lube import fetch
from intcode import Intcode

# 109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99
# should output a copy of itself.
t = Intcode([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99])
t.run()
assert t.output == [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]

# 1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number.
t = Intcode([1102, 34915192, 34915192, 7, 4, 7, 99, 0])
t.run()
assert len(str(t.output.pop())) == 16

# 104,1125899906842624,99 should output the large number in the middle.
t = Intcode([104, 1125899906842624, 99])
t.run()
assert t.output.pop() == 1125899906842624


#The BOOST program will ask for a single input; run it in test mode by providing it the value 1.
# It will perform a series of checks on each opcode, output any opcodes (and the associated parameter modes) that
# seem to be functioning incorrectly, and finally output a BOOST keycode.
s = fetch(2019, 9)
program = list(map(int, s.split(',')))
p = Intcode(program.copy())
p.add_input(1)
p.run()
print(f"Part 1: {p.output.pop()}")

# The program runs in sensor boost mode by providing the input instruction the value 2. Once run, it will boost the
# sensors automatically, but it might take a few seconds to complete the operation on slower hardware. In sensor boost
# mode, the program will output a single value: the coordinates of the distress signal.
p = Intcode(program.copy())
p.add_input(2)
p.run()
print(f"Part 2: {p.output.pop()}")

