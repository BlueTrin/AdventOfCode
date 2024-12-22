# typed on a phone with intermittent connection

import functools
import sys
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


sys.setrecursionlimit(3000)

@functools.lru_cache(maxsize=None)
def evolve(d, depth):
    if depth != 0:
        d = evolve(d, depth-1)
    d = d ^ (d * 64)
    d = d % 16777216

    d = d ^ (d // 32)
    d = d % 16777216

    d = d ^ (d * 2048)
    d = d % 16777216

    return d


inp = '''1
10
100
2024'''

total=0
for r in inp.splitlines():
    sub = evolve(int(r), 1999)
    # print(f"{r}: {sub}")
    total += sub

print(total)

def build_seq2score(r, maxdepth):
    seq2score = {}
    sequence = [int(r) % 10]+[evolve(int(r), d)%10 for d in range(maxdepth)]
    for it in range(4, len(sequence)):
        key = tuple(sequence[it-shift] - sequence[it-shift-1] for shift in reversed(range(4)))
        if key not in seq2score:
            seq2score[key] = sequence[it]
    return seq2score

    
def part12(inp):
    total=0
    
    seq_score=[]
    lenlines = len(inp.splitlines())
    for i, r in enumerate(inp.splitlines()):
        logger.info(f"{i} out of {lenlines}")
        scores = {}
        sub = evolve(int(r), 1999)
        # print(f"{r}: {sub}")
        total += sub
        seq_score.append(build_seq2score(int(r), 2000))
    print("part1", total)
    
    from collections import defaultdict
    seq2globalscore = defaultdict(int)
    for i_col, oneseq2score in enumerate(seq_score):
        logger.info(f"{i_col}/{len(seq_score)}")
        for seq, score in oneseq2score.items():
            seq2globalscore[seq] += score

    max_score = max(seq2globalscore.values())
    bestseq = [k for k, v in seq2globalscore.items() if v==max_score]

    return total, max_score, bestseq, len(seq_score[0])

res = build_seq2score(123, 9)
print(res)
# raise RuntimeError("test")

from pprint import pp
pp(res)

# raise RuntimeError("toto")


inp = """1
2
3
2024"""

_, max_bananas, seq, _ = part12(inp)


if max_bananas != 23:
    raise RuntimeError(f"failed test max {max_bananas} {seq}")


inp = open("2024_22.txt").read()
print(part12(inp))

