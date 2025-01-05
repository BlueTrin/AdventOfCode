from aoc_lube import fetch
import re
from collections import defaultdict, deque


s = fetch(2018, 9)
players, last_marble = [int(x) for x in re.findall(r'\d+', s)]

def solve(players, last_marble):
    d = deque([0])

    score = defaultdict(int)

    next_marble = 0
    curr = 0
    while next_marble != last_marble:
        next_marble += 1
        if next_marble % 23 == 0:
            # However, if the marble that is about to be placed has a number which is a multiple of 23, something
            # entirely different happens. First, the current player keeps the marble they would have placed, adding
            # it to their score. In addition, the marble 7 marbles counter-clockwise from the current marble is removed
            # from the circle and also added to the current player's score. The marble located immediately clockwise of
            # the marble that was removed becomes the new current marble.
            d.rotate(7)
            score[next_marble % players] += next_marble + d.popleft()
    #        d = d[:idx] + d[idx+1:]
        else:
            #hen, each Elf takes a turn placing the lowest-numbered remaining marble into the circle between the marbles
            # that are 1 and 2 marbles clockwise of the current marble. (When the circle is large enough, this means that
            # there is one marble between the marble that was just placed and the current marble.) The marble that was just
            # placed then becomes the current marble.
            d.rotate(-2)
            d.appendleft(next_marble)

    return max(score.values())

assert solve(9, 25) == 32
# players, last_marble = 10, 1618
# players, last_marble = 13, 7999
print(f"Part 1: {solve(players, last_marble)}")
print(f"Part 2: {solve(players, last_marble*100)}")