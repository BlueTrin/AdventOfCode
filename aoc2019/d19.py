from aoc_lube import fetch
from intcode import Intcode


s = fetch(2019, 19)

prog = list(map(int, s.strip().split(',')))

comp = Intcode(prog)
pull = {}
for x in range(50):
    for y in range(50):
        comp.reset()
        comp.add_input(x)
        comp.add_input(y)
        comp.run()
        pull[(x, y)] = comp.output.pop()

print(sum(pull.values()))

for y in range(50):
    print(''.join('#' if pull[(x, y)] else '.' for x in range(50)))


def is_pulled(x, y):
    comp.reset()
    comp.add_input(x)
    comp.add_input(y)
    comp.run()
    return comp.output.pop()

def len_pulled(x):
    top = int(x*0.7)
    inarea = int(x*0.82)
    assert is_pulled(x, top) == 0
    assert is_pulled(x, inarea) == 1

    while inarea-top >1:
        mid = (top+inarea)//2
        if is_pulled(x, mid):
            inarea = mid
        else:
            top = mid
    in_top = inarea

    in_bot = int(x*0.82)
    bottom = x
    assert is_pulled(x, bottom) == 0
    while bottom-in_bot >1:
        mid = (bottom+in_bot)//2
        if is_pulled(x, mid):
            in_bot = mid
        else:
            bottom = mid
    return in_top, in_bot


x_start = 600
x_end = 1200

while x_end-x_start > 1:
    mid = (x_start+x_end)//2
    in_top, in_bot = len_pulled(mid)
    in_top2, in_bot2 = len_pulled(mid+99)

    if in_bot-in_top2 >= 99:
        x_end = mid
    else:
        x_start = mid

print(len_pulled(x_end))
print(len_pulled(x_end+99))

# top left square
print(f'Part 2: {x_end*10000 + len_pulled(x_end+99)[0]}')

