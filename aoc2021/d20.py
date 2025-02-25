from aoc_lube import fetch
from utils.utils import Point
from collections import defaultdict
import itertools

s = fetch(2021, 20)

example = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###'''

def read_s(s):
    algo_s, img_s = s.split('\n\n')

    algo = {}
    for i, c in enumerate(algo_s):
        algo[i] = {'.': '0', '#': '1'}[c]

    img = defaultdict(lambda : '0')
    for iy, row in enumerate(img_s.splitlines()):
        for ix, c in enumerate(row):
            v = {'.': '0', '#': '1'}[c]
            if v == '1':
                img[Point(ix, iy)] = v

    return algo, img

def enhance(algo, img, round):
    res = defaultdict(int)
    for p in tuple(img.keys()):
        for dpx, dpy in itertools.product(range(-1, 2), repeat=2):
            n = p + Point(dpx, dpy)
            if n in res:
                continue
            s = ''.join([img[n + Point(dx, dy)] for dy in range(-1, 2) for dx in range(-1, 2)])
            res[n] = algo[int(s, 2)]

    # real example threw a curve ball, 0 becomes 1 in the algo ...
    # so all 0s becomes 1s in the result in the far away regions then they become 0 the next round
    if round % 2 == 1 and algo[0] == '1':
        default_val = '1'
    else:
        default_val = '0'

    if default_val == '1':
        res = defaultdict(lambda: default_val, {k:v for k, v in res.items()})
    else:
        res = defaultdict(lambda: default_val, {k:v for k, v in res.items() if v == '1'})
    return res

def print_img(img):
    minx = min(x for x, y in img)
    miny = min(y for x, y in img)
    maxx = max(x for x, y in img)
    maxy = max(y for x, y in img)

    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            print('#' if img[Point(x, y)] == '1' else '.', end='')
        print()

algo, img = read_s(example)
img = enhance(algo, img, round=1)
img = enhance(algo, img, round=2)
print_img(img)

algo, img = read_s(s)
for i in range(1, 51):
    print(f"Round {i}")
    img = enhance(algo, img, round=i)
    if i == 2:
        p1 = sum(1 for v in img.values() if v == '1')
print_img(img)
print(f"Part1: {p1}")
# 5488 too high

p2 = sum(1 for v in img.values() if v == '1')
print(f"Part2: {p2}")
# print_img(img)
pass