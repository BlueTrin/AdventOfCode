from aoc_lube import fetch
import re
from collections import Counter

s = fetch(2017, 7)

t = {}
tree = {}
sweights = {}

for r in s.splitlines():
    n, w, *children = [x for x in re.split(' \(|\)| -> |, ', r) if x]
    for c in children:
        t[c] = n
    tree[n] = children
    sweights[n] = int(w)

print(f"Part1: {set(t.values()) - set(t)}")

vals = {}

for n in set(t) - set(t.values()):
    assert len(tree[n]) == 0
    vals[n] = sweights[n]

while len(vals) < len(tree):
    for n in set(tree) - set(vals):
        if all(c in vals for c in tree[n]):
            vals[n] = sweights[n] + sum(vals[c] for c in tree[n])

    for n, children in tree.items():
        if all(c in vals for c in children):
            weights = [vals[c] for c in children]
            if len(set(weights)) > 1:
                oddweight = [k for k, v in Counter(weights).items() if v == 1][0]
                tgtweight = [k for k, v in Counter(weights).items() if v != 1][0]

                badweight = [sweights[c] for c in children if vals[c] == oddweight][0]
                print(f"Part2: {badweight + (tgtweight-oddweight)}")
                raise RuntimeError("I R DUN")
pass