from aoc_lube import fetch
from utils.utils import Point

s = fetch(2018, 18)

print(s)
m = {}
for y, r in enumerate(s.splitlines()):
    if not r:
        continue
    for x, c in enumerate(r):
        m[Point(x, y)] = c

orig_m = m.copy()

for i in range(10):
    m2 = {}
    for pt, c in m.items():
        if c == '.':
            if sum([1 for i in pt.adjacent8() if m.get(i, '') == '|']) >= 3:
                m2[pt] = '|'
            else:
                m2[pt] = '.'
        if c == '|':
            if sum([1 for i in pt.adjacent8() if m.get(i, '') == '#']) >= 3:
                m2[pt] = '#'
            else:
                m2[pt] = '|'
        if c == '#':
            if sum([1 for i in pt.adjacent8() if m.get(i, '') == '#']) >= 1 and sum([1 for i in pt.adjacent8() if m.get(i, '') == '|']) >= 1:
                m2[pt] = '#'
            else:
                m2[pt] = '.'
    m = m2

print(sum([1 for c in m.values() if c == '|']) * sum([1 for c in m.values() if c == '#']))


m = orig_m.copy()

for i in range(1, 1000000000):
    m2 = {}
    for pt, c in m.items():
        if c == '.':
            if sum([1 for i in pt.adjacent8() if m.get(i, '') == '|']) >= 3:
                m2[pt] = '|'
            else:
                m2[pt] = '.'
        if c == '|':
            if sum([1 for i in pt.adjacent8() if m.get(i, '') == '#']) >= 3:
                m2[pt] = '#'
            else:
                m2[pt] = '|'
        if c == '#':
            if sum([1 for i in pt.adjacent8() if m.get(i, '') == '#']) >= 1 and sum([1 for i in pt.adjacent8() if m.get(i, '') == '|']) >= 1:
                m2[pt] = '#'
            else:
                m2[pt] = '.'
    m = m2

    if i % 100 == 0:
        print(i, sum([1 for c in m.values() if c == '|']) * sum([1 for c in m.values() if c == '#']))

# 0 269005
# 100 107198
# 200 119085
# 300 205500
# 400 154882
# 500 174264
# 600 191070
# 700 174945
# 800 211344
# 900 168960
# 1000 202768
# 1100 176134
# 1200 174264
# 1300 191070
# 1400 174945
# 1500 211344
# 1600 168960
# 1700 202768
# 1800 176134
# 1900 174264
# 2000 191070
# 2100 174945
# 2200 211344
# 2300 168960
# 2400 202768  too low
# 2500 176134
# 2600 174264
# 2700 191070
# 2800 174945
# 2900 211344
# 3000 168960
# 3100 202768
# 3200 176134
# 3300 174264