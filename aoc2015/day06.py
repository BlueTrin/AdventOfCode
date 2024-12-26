import re
from collections import defaultdict


def part12(part1=True):
    if part1:
        d = defaultdict(bool)
    else:
        d = defaultdict(int)
    print(f"on={sum(d.values())}")

    for r in open("2015_06.txt").read().splitlines():
        m = re.match(r"(?P<comm>turn on|turn off|toggle) "
                     r"([\d]{0,3}),([\d]{0,3}) through ([\d]{0,3}),([\d]{0,3})", r)
        comm, x1, y1, x2, y2 = m.groups()

        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        assert x2 >= x1
        assert y2 >= y1
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                if part1 and comm == "turn on":
                    d[(x, y)] = True
                elif part1 and comm == "turn off":
                    d[(x, y)] = False
                elif part1 and comm == "toggle":
                    d[(x, y)] = not d[(x, y)]
                elif comm == "turn on":
                    d[(x, y)] += 1
                elif comm == "turn off":
                    d[(x, y)] = max(0, d[(x, y)]-1)
                elif comm == "toggle":
                    d[(x, y)] += 2

    return sum(d.values())


print(part12())
print(part12(False))
