from aoc_lube import fetch
from collections import Counter

s = fetch(2021, 14)
test = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''

def p1solve(s):
    start, conv_s = s.split('\n\n')
    conv = {k: v for k, v in [x.split(' -> ') for x in conv_s.splitlines()]}

    ch = start
    for _ in range(10):
        n = ""
        for c1, c2 in zip(ch, ch[1:]):
            n += c1 + conv.get(c1+c2, '')
        n += start[-1]
        ch = n

    c = Counter(ch)
    return max(c.values())-min(c.values())

p1 = p1solve(s)
print(f"Part1: {p1}")

def p2_solve(s, steps=40):
    start, conv_s = s.split('\n\n')
    conv = {k: v for k, v in [x.split(' -> ') for x in conv_s.splitlines()]}
    c = Counter()
    for c1, c2 in zip(start, start[1:]):
        c[c1+c2] += 1

    for _ in range(steps):
        n = Counter()
        for (c1, c2), v in c.items():
            l = conv.get(c1+c2)

            if l is None:
                n[c1+c2] += v
            else:
                n[c1+l] += v
                n[l+c2] += v
        c = n

    # we count the characters, all characters are twice since we had them 2 by 2 except the first and last
    l_count = Counter((start[0], start[-1]))
    for (c1, c2), v in c.items():
        l_count[c1] += v
        l_count[c2] += v
    for c, v in l_count.items():
        l_count[c] //= 2

    return max(l_count.values())-min(l_count.values())

assert p2_solve(test, 10) == 1588

assert p2_solve(test) == 2188189693529
p2 = p2_solve(s)
print(f"Part2: {p2}")
# 1518281887937 too low?