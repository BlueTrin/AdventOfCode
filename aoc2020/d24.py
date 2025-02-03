from aoc_lube import fetch
from collections import deque
import numpy as np
from collections import defaultdict


s = fetch(2020, 24)

# s = '''sesenwnenenewseeswwswswwnenewsewsw
# neeenesenwnwwswnenewnwwsewnenwseswesw
# seswneswswsenwwnwse
# nwnwneseeswswnenewneswwnewseswneseene
# swweswneswnenwsewnwneneseenw
# eesenwseswswnenwswnwnwsewwnwsene
# sewnenenenesenwsewnenwwwse
# wenwwweseeeweswwwnwwe
# wsweesenenewnwwnwsenewsenwwsesesenwne
# neeswseenwwswnwswswnw
# nenwswwsewswnenenewsenwsenwnesesenew
# enewnwewneswsewnwswenweswnenwsenwsw
# sweneswneswneneenwnewenewwneswswnese
# swwesenesewenwneswnwwneseswwne
# enesenwswwswneneswsenwnewswseenwsese
# wnwnesenesenenwwnenwsewesewsesesew
# nenewswnwewswnenesenwnesewesw
# eneswnwswnwsenenwnwnwwseeswneewsenese
# neswnwewnwnwseenwseesewsenwsweewe
# wseweeenwnesenwwwswnew'''

DIR_TO_COORD = {
    'e': np.array([0, 2]),
    'w': np.array([0, -2]),

    'ne': np.array([-1, 1]),
    'se': np.array([1, 1]),

    'nw': np.array([-1, -1]),
    'sw': np.array([1, -1]),
}

flip = defaultdict(bool)

for r in s.splitlines():
    de = deque(r)
    curr = np.array([0, 0])
    while de:
        di = de.popleft()
        if di == 's' or di == 'n':
            di += de.popleft()
        curr += DIR_TO_COORD[di]
    flip[tuple(curr)] = not flip[tuple(curr)]
    # print(curr, sum(flip.values()))
    # pass

print(f"Part1: {sum(flip.values())}")

for _ in range(100):
    count_black = defaultdict(int)
    for k, v in list(flip.items()):
        if not v:
            continue
        for d in DIR_TO_COORD.values():
            count_black[tuple(k + d)] += 1

    new_flip = defaultdict(bool)
    for k, v in list(flip.items()):
        if not v:
            continue
        # Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
        if count_black[k] == 0 or count_black[k] > 2:
            continue
        new_flip[k] = True
    for k, v in count_black.items():
        # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
        if v == 2 and not flip[k]:
            new_flip[k] = True
    flip = new_flip

print(f"Part2: {sum(flip.values())}")
