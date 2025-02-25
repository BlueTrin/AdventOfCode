from aoc_lube import fetch
from functools import cache
import itertools
from typing import Tuple

s = fetch(2021, 21)

st1, st2 = [int(r.split()[-1]) for r in s.splitlines()]

print(st1, st2)

s1 = 0
s2 = 0

dice = 1
rolls = 0

def next_dice(d):
    v = [(n-1)%100+1 for n in range(d, d+4)]
    return v[-1], sum(v[0:3])

# example from the page
# st1, st2 = 4, 8

while True:
    dice, s = next_dice(dice)
    rolls += 3
    st1 += s
    st1 = (st1-1)%10 + 1
    s1 += st1
    if s1 >= 1000:
        break

    dice, s = next_dice(dice)
    rolls += 3
    st2 += s
    st2 = (st2-1)%10 + 1
    s2 += st2
    if s2 >= 1000:
        break

print(f"Part1: {min(s1, s2) * rolls}")

@cache
def count_paths(score1, score2, pos1, pos2) -> Tuple[int, int]:
    wins1 = 0
    wins2 = 0

    for d1, d2, d3 in itertools.product(range(1, 4), repeat=3):
        new_pos1 = (pos1 - 1 + d1 + d2 + d3) % 10 + 1
        new_score1 = score1 + new_pos1
        if new_score1 >= 21:
            wins1 += 1
            continue
        else:
            # we flip around to player 2 turn
            next_wins2, next_wins1 = count_paths(score2, new_score1, pos2, new_pos1)
            wins1 += next_wins1
            wins2 += next_wins2

    return wins1, wins2

@cache
def count_wins(position_1, position_2, score_1, score_2):
    wins_1 = 0
    wins_2 = 0
    for roll_1, roll_2, roll_3 in itertools.product((1, 2, 3), repeat=3):
        new_position_1 = (position_1 - 1 + roll_1 + roll_2 + roll_3) % 10 + 1
        new_score_1 = score_1 + new_position_1
        if new_score_1 >= 21:
            wins_1 += 1
        else:
            new_wins_2, new_wins_1 = count_wins(position_2, new_position_1, score_2, new_score_1)
            wins_1 += new_wins_1
            wins_2 += new_wins_2
    return wins_1, wins_2

s = fetch(2021, 21)

st1, st2 = [int(r.split()[-1]) for r in s.splitlines()]
wins1, wins2 = count_paths(0, 0, st1, st2)
print(f"Part2: {max(wins1, wins2)}")