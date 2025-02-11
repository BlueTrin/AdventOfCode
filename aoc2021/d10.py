from aoc_lube import fetch
from collections import deque

s =fetch(2021, 10)

# s = '''[({(<(())[]>[[{[]{<()<>>
# [(()[<>])]({[<{<<[]>>(
# {([(<{}[<>[]}>{[]{[(<()>
# (((({<>}<{<{<>}{[]{[]{}
# [[<[([]))<([[{}[[()]]]
# [{[{({}]{}}([{[{{{}}([]
# {<[[]]>}<{[{[{[]{()[[[]
# [<(<(<(<{}))><([]([]()
# <{([([[(<>()){}]>(<<{{
# <{([{{}}[<[[[<>{}]]]>[]]'''

CLOSE_TO_OPEN = {')': '(', ']': '[', '}': '{', '>': '<'}
OPEN_TO_CLOSE = {v: k for k, v in CLOSE_TO_OPEN.items()}

# ): 3 points.
# ]: 57 points.
# }: 1197 points.
# >: 25137 points.
SCORE = {')': 3, ']': 57, '}': 1197, '>': 25137}

# ): 1 point.
# ]: 2 points.
# }: 3 points.
# >: 4 points.
P2_SCORE = {')': 1, ']': 2, '}': 3, '>': 4}

score = 0
p2 = []
for r in s.splitlines():
    st = deque()

    for c in r:
        if c in '{[<(':
            st.append(c)
        elif c in ')]>}':
            if CLOSE_TO_OPEN[c] != st.pop():
                score += SCORE[c]
                break
    else:
        # ): 1 point.
        # ]: 2 points.
        # }: 3 points.
        # >: 4 points.
        row_score = 0
        while st:
            row_score *= 5
            row_score += P2_SCORE[OPEN_TO_CLOSE[st.pop()]]
        p2.append(row_score)

print(f"Part1: {score}")
# 367227

print(f"Part2: {sorted(p2)[len(p2)//2]}")
# 337138329597 too high



