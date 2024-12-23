import itertools
from pprint import pformat
from collections import defaultdict, deque

def nwsize_dq(conns, debug=False):
    q = deque()
    max_nw = 0
    sol = None
    seen = set()
    q.extendleft((n,) for n in conns.keys())
    
    while q:
        nw = q.pop()
        if nw in seen:
            continue
        seen.add(nw)
        if debug:
            print(nw)
            print(seen)
        try:
            cand_lst = set.intersection(*(conns[n] for n in nw))
        except Exception as e:
            print(f"nw={nw}")
            raise
        
        if cand_lst:
            q.extend(tuple(sorted(nw+(cand,)))
                         for cand in cand_lst
                         if tuple(sorted(nw+(cand,))) not in seen)
                    
        else:
            max_nw, sol = (len(nw), ",".join(nw)) if len(nw) > max_nw else (max_nw, sol)         
    return max_nw, sol

def part1(inp, debug=False):
    conns = defaultdict(set)
    allnets = set()
    for r in inp.splitlines():
        if not r:
            continue
        n1, n2 = r.split('-')
        conns[n1].add(n2)
        conns[n2].add(n1)

    total = len(set(tuple(sorted([n1, n2, n3]))
                for n1, n1conns in conns.items()
                for n2 in n1conns if n1.startswith('t')
                for n3 in set.intersection(n1conns, conns[n2])))
    print(total)
    print(nwsize_dq(conns, debug))
    

inp="""kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

part1(inp, debug=True)


part1(open("2024_23.txt").read())