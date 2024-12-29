import numpy as np
from scipy.signal import convolve2d
from aoc_lube import fetch
from scipy.stats import pareto

s = fetch(2015, 18)

s_ex = '''.#.#.#
...##.
#....#
..#...
#.#..#
####..'''


kernel = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]])

def next_iter(m, part2=False):
    if part2:
        m[0, 0] = 1
        m[0, -1] = 1
        m[-1, 0] = 1
        m[-1, -1] = 1
    neighmap = convolve2d(m, kernel, mode='same', boundary='fill', fillvalue=0)
    res =  np.array([[1 if (x and y ==2 or y ==3 ) or (not x and y ==3) else 0 for x, y in zip(state_row, neighbour_row)]
                     for  state_row, neighbour_row in zip(m, neighmap)])
    if part2:
        res[0, 0] = 1
        res[0, -1] = 1
        res[-1, 0] = 1
        res[-1, -1] = 1
    return res


m = np.array([list(int(c == '#') for c in x) for x in s.splitlines()])
for i in range(100):
    m = next_iter(m)
print(np.sum(m))

m_ex = np.array([list(int(c == '#') for c in x) for x in s_ex.splitlines()])
for i in range(5):
    m_ex = next_iter(m_ex, part2=True)
    print(m_ex)
print(np.sum(m_ex))

m = np.array([list(int(c == '#') for c in x) for x in s.splitlines()])
for i in range(100):
    m = next_iter(m, part2=True)
print(np.sum(m))
