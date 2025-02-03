from aoc_lube import fetch
from collections import deque

s = fetch(2020, 23)

print(s)

def play(cups, rounds, p2=False):
    next_cup = {}
    prev_cup = {}

    lb = min(cups)
    hb = max(cups)

    for i in range(0, len(cups)):
        next_cup[cups[i-1]] = cups[i]
        prev_cup[cups[i]] = cups[i-1]

    curr = cups[0]
    for i in range(rounds):
        cut_start_cup = next_cup[curr]
        mid_cup = next_cup[cut_start_cup]
        cut_end_cup = next_cup[mid_cup]
        next_cur = next_cup[cut_end_cup]

        next_cup[curr] = next_cur
        prev_cup[next_cur] = curr

        insert_cup = curr - 1
        while insert_cup < lb or  insert_cup in {cut_start_cup, mid_cup, cut_end_cup}:
            insert_cup -= 1
            if insert_cup < lb:
                insert_cup = hb

        insert_after = next_cup[insert_cup]
        next_cup[insert_cup] = cut_start_cup
        prev_cup[cut_start_cup] = insert_cup
        next_cup[cut_end_cup] = insert_after
        prev_cup[insert_after] = cut_end_cup

        curr = next_cur
        # print_cups(curr, next_cup, prev_cup)

    if p2:
        return next_cup[1] * next_cup[next_cup[1]]
    else:
        s = ""
        it = next_cup[1]
        while it != 1:
            s += str(it)
            it = next_cup[it]
        return s

def print_cups(cur, next_cups, prev_cups):
    it = cur
    while True:
        print(it, end=' ')
        it = next_cups[it]
        if it == cur:
            print()
            break

def read_cups(s, p2=False):
    return list(map(int, s)) + (list(range(10, 1000001)) if p2 else [])

res = play(read_cups("389125467"), 10)
assert res == "92658374"

res = play(read_cups(s), 100)
print(f"Part1: {res}")

res = play(read_cups(s, p2=True), 10000000, p2=True)
print(f"Part2: {res}")
