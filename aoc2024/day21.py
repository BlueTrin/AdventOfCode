from collections import namedtuple
from functools import lru_cache
from itertools import product
class Point(namedtuple('Point',['x', 'y'])):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y )

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


# Keypads
NUMPAD = {k:Point(i%3, (3-i//3)) for i, k in enumerate("789456123 0A")}
DIRPAD = {k:Point(i%3, (3-i//3)) for i, k in enumerate(" ^A<v>")}

'''
Returns only sequences that have repeating characters
'''
def best(start, end, keypad):
    pt_a, pt_v, pt_space = keypad[start], keypad[end], keypad[' ']
    pt_diff = pt_v - pt_a

    toret = set()

    v_seq = pt_diff.y * '^' + 'v' * - pt_diff.y
    h_seq = pt_diff.x * '>' + '<' * - pt_diff.x

    # if we end up on space don't add the step
    if pt_a + Point(0, pt_diff.y) != pt_space:
        toret.add(v_seq + h_seq + "A")
    if pt_a + Point(pt_diff.x, 0) != pt_space:
        toret.add(h_seq + v_seq + "A")
    return toret

'''
Get a list of moves for a combination and a certain keypad
for example c = '805A' and keypad = NUMPAD
Assumption is that we start on 'A' 
'''
def moves(c, keypad):
    return {"".join(x) for x in product(*[best(*p, keypad)
                                          for p in zip("A"+c, c)])}

@lru_cache(maxsize=None)
def count(m, depth):
    if depth == 0: return len(m)
    return sum( min(count(s, depth-1) for s in moves(part+"A", DIRPAD))
              for part in m[:-1].split("A"))


def part1(inp):
    total = 0
    depth = 2
    for code in inp.splitlines():
        total += int(code[:-1]) * min(count(move, depth) for move in moves(code, NUMPAD))
    return total

def part2(inp):
    total = 0
    depth = 25
    for code in inp.splitlines():
        total += int(code[:-1]) * min(count(move, depth) for move in moves(code, NUMPAD))
    return total

from aoc_lube import fetch
inp = fetch(2024, 21)
print(part1(inp))
print(part2(inp))
