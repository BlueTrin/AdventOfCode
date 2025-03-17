from aoc_lube import fetch
import re
import numpy
import logging
import functools
from collections import deque

logging.basicConfig(format='%(asctime)s %(message)s')

logger = logging.getLogger(__name__)


s = fetch(2021, 24)
#print(s)

code_blocks = ["inp w" + block for block in s.split("inp w") if block]

BLOCK_TYPE1 = r'inp w\nmul x 0\nadd x z\nmod x 26\ndiv z 1\nadd x (-?\d+)\neql x w\neql x 0\nmul y 0\nadd y 25\nmul y x\nadd y 1\nmul z y\nmul y 0\nadd y w\nadd y (-?\d+)\nmul y x\nadd z y\n?'
BLOCK_TYPE2 = r'inp w\nmul x 0\nadd x z\nmod x 26\ndiv z 26\nadd x (-?\d+)\neql x w\neql x 0\nmul y 0\nadd y 25\nmul y x\nadd y 1\nmul z y\nmul y 0\nadd y w\nadd y (-?\d+)\nmul y x\nadd z y\n?'

@functools.cache
def block1(old_z, w, inp1, inp2, debug=False):
    '''
    If z % 26 != (w + inp1):
       * z appends (w + inp2)
       * otherwise z is unchanged
    '''
    x = old_z % 26 + inp1
    if x != w:
        if debug:
            logger.info(f"z%26+{inp1}={x} != {w}")
        old_z *= 26
        old_z += w + inp2
    else:
        if debug:
            logger.info(f"z%26+{inp1}={x} == {w}")

    return old_z

@functools.cache
def block2(old_z, w, inp1, inp2, debug=False):
    '''
    If z % 26 != (w + inp1):
       * z replaces last digit with (w + inp2)
       * otherwise z loses right digit
    '''
    z = old_z
    x = z % 26 + inp1

    z //= 26

    if x != w:
        if debug:
            logger.info(f"z%26+{inp1}={x} != {w}")

        z *= 26
        z += w + inp2
    else:
        if debug:
            logger.info(f"z%26+{inp1}={x} == {w}")

    return z


program_struct = []
for i, block in enumerate(code_blocks):
    if m:=re.match(BLOCK_TYPE1, block):
        program_struct.append((1,) + tuple(map(int, m.groups())))
        print(f"{i} is Type1 with {m.groups()}")
        continue
    elif m:=re.match(BLOCK_TYPE2, block):
        program_struct.append((2,) + tuple(map(int, m.groups())))
        print(f"{i} is Type2 with {m.groups()}")
        continue
    else:
        raise RuntimeError("Unknown block type")

v = block2(26, -12, -12, 2)

inp = '0' * 14
def solve(inp, s, debug=False, verbose=False):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    vars = {
        'w': 0,
        'x': 0,
        'y': 0,
        'z': 0,
    }
    for r in s.splitlines():
        cmd, *args = r.split()
        if cmd == 'inp':
            vars[args[0]] = int(inp[0])
            inp = inp[1:]
        elif cmd == 'add':
            if args[1] not in vars:
                vars[args[0]] += int(args[1])
            else:
                vars[args[0]] += vars[args[1]]

        elif cmd == 'mul':
            if args[1] not in vars:
                vars[args[0]] *= int(args[1])
            else:
                vars[args[0]] *= vars[args[1]]

        elif cmd == 'div':
            if args[1] not in vars:
                vars[args[0]] //= int(args[1])
            else:
                vars[args[0]] //= vars[args[1]]

        elif cmd == 'mod':
            if args[1] not in vars:
                vars[args[0]] %= int(args[1])
            else:
                vars[args[0]] %= vars[args[1]]

        elif cmd == 'eql':
            if args[1] not in vars:
                vars[args[0]] = int(vars[args[0]] == int(args[1]))
            else:
                vars[args[0]] = int(vars[args[0]] == vars[args[1]])

        else:
            raise ValueError(f"Unknown command: {cmd}")

        if verbose:
            logger.debug(f"{r} -> {vars}")

        if r == 'add z y':
            logger.debug(f"z(base26)={numpy.base_repr(vars['z'], 26)}")
    return vars


res = solve('6', '''inp x
mul x -1''')
assert res['x'] == -6

res = solve('13', '''inp z
inp x
mul z 3
eql z x''')
assert res['z'] == 1

res = solve('7', '''inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2''')
assert res == {'w': 0, 'x': 1, 'y': 1, 'z': 1}
sol = ''

while len(sol) < 14:
    sol += min([(solve(sol + c + '1' * 14, s)['z'], c) for c in '123456789'])[1]


def exec_short(program_struct, sol, debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    z = 0
    for step, d in zip(program_struct, sol):
        if step[0] == 1:
            z = block1(z, int(d), *map(int, step[1:]))
        else:
            z = block2(z, int(d), *map(int, step[1:]))
        logger.debug(f"z(base26)={numpy.base_repr(z, 26)}")

    return z
# 11181211197131 not working
print(sol)
print(solve(sol, s, debug=True))
print(exec_short(program_struct, sol, debug=True))


# solution for 0 and 13
z = 0
w0 = 7
w13 = 6 + w0 - 12
z = block1(z, w0, 12, 6)
print(numpy.base_repr(z, 26))
z = block2(z, w13, -12, 2, debug=True)
print(numpy.base_repr(z, 26))


solutions = {}
d = deque()
for i, step_i in enumerate(program_struct):

    if step_i[0] == 1:
        d.append(i)
    elif step_i[0] == 2:
        j = d.pop()
        step_j = program_struct[j]

        # change reversed to find the largest solution
        for sol_j in range(1, 10):
            for sol_i in range(1, 10):
                z = 0
                z = block1(z, sol_j, *step_j[1:])
                z = block2(z, sol_i, *step_i[1:])
                if z == 0:
                    solutions[j] = sol_j
                    solutions[i] = sol_i
                    logger.info(f"solutions[{j}]={sol_j}")
                    logger.info(f"solutions[{i}]={sol_i}")
                    break
            else:
                continue
            break
        else:
            raise RuntimeError("No solution found")
sol = ''.join(list(str(solutions[i]) for i in range(14)))
print(sol)
print(solve(sol, s, debug=False))
# 99298993199873 largest
# 73181221197111 smallest

pass
# 0 is Type1 with ('12', '6')
# 1 is Type1 with ('10', '2')
# 2 is Type1 with ('10', '13')

# 3 is Type2 with ('-6', '8')

# 4 is Type1 with ('11', '13')

# 5 is Type2 with ('-12', '8')

# 6 is Type1 with ('11', '3')
# 7 is Type1 with ('12', '11')
# 8 is Type1 with ('12', '10')

# 9 is Type2 with ('-2', '8')
# 10 is Type2 with ('-5', '14')
# 11 is Type2 with ('-4', '6')

# 12 is Type2 with ('-4', '8')

# 13-21 + 1-9
# 13 is Type2 with ('-12', '2')

