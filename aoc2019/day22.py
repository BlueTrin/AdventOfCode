
from aoc_lube import fetch

i = fetch(2019, 22)
def part1(i, order):
    stack = [i for i in range(order)]
    for line in i.split('\n'):
        if line.startswith('deal into new stack'):
            stack = stack[::-1]
        elif line.startswith('cut'):
            n = int(line.split()[-1])
            stack = stack[n:] + stack[:n]
        elif line.startswith('deal with increment'):
            n = int(line.split()[-1])
            new_stack = [0] * len(stack)
            for i, card in enumerate(stack):
                new_stack[(i * n) % len(stack)] = card
            stack = new_stack
    print(stack.index(2019))

part1(i, 10007)
part1(i, 119315717514047)
