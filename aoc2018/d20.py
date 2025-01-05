from aoc_lube import fetch
from collections import deque
from utils.utils import Point
import networkx as nx


s = fetch(2018, 20)

print(s)
lens = {}
G = nx.Graph()

DIR2PT = {
    'N': Point(0, -1),
    'S': Point(0, 1),
    'E': Point(1, 0),
    'W': Point(-1, 0),
}

def find_matching_paren(s, idx):
    stack = []
    pipes = []
    for i, c in enumerate(s[idx:]):
        if c == '|' and not stack:
            pipes.append(i)
        if c == '(':
            stack.append(i)
        if c == ')':
            if not stack:
                return i, pipes
            stack.pop()
    return None, pipes

def process(s):
    d = deque()
    d.append((Point(0, 0), s, 0))
    while d:
        mins = {}
        for k, v, l in d:
            if (k, v) not in mins:
                mins[(k, v)] = l
            else:
                mins[(k, v)] = min(l, mins[(k, v)])

        pt, s, l = d.popleft()
        if l > mins[(pt, s)]:  # Skip if we have already been here
            continue

        idx_par, pipes = find_matching_paren(s, 0)
        assert idx_par is None
        if pipes:
            for tkn in [s[start + 1:end] for start, end in zip([-1] + pipes, pipes + [len(s)])]:
                d.append((pt, tkn + s[idx + 1:], l))
            continue

        if s[0] in '^$':
            s = s[1:]

        while s and s[0] in DIR2PT:
            c = s[0]
            s = s[1:]
            G.add_edge(pt, pt + DIR2PT[c])
            pt += DIR2PT[c]
            l+=1
            lens[pt] = min(lens.get(pt, 1000000), l)

        if s:
            c = s[0]
            s = s[1:]
            if c in '$^':
                continue
            elif c == '(':
                idx, pipes = find_matching_paren(s, 0)
                for tkn in [s[start+1:end] for start, end in zip([-1]+pipes, pipes+[idx])]:
                    if (pt, tkn + s[idx+1:], l) not in d:
                        d.append((pt, tkn + s[idx+1:], l))

            elif c == '|':
                raise NotImplementedError("Not implemented")
            else:
                raise NotImplementedError("Not implemented")

#        print(pt, s)


process(s)
#
# l, pt = sorted([(v,k) for k,v in lens.items()], reverse=True)[0]
# max_len = nx.shortest_path_length(G, Point(0, 0), pt)
# c = 0
# for l, pt in sorted([(v,k) for k,v in lens.items()], reverse=True):
#     if l >= 1000:
#         real_l = nx.shortest_path_length(G, Point(0, 0), pt)
#         max_len = max(max_len, real_l)
#         if real_l >= 1000:
#             c += 1
#
# print(max_len)
# print(c)

fill = {
    0: {Point(0, 0)}
}
lvl = 1
while True:
    neighbors = set(x for pt in fill[lvl-1] for x in G.neighbors(pt)) - fill[lvl-1] - fill.get(lvl-2, set())
    if len(neighbors) == 0:
        break

    fill[lvl] = neighbors
    lvl += 1
print("Part1: ", max(fill.keys()))
print("Part2: ", sum([len(fill[lvl]) for lvl in range(1000, max(fill.keys())+1)]))