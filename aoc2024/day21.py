import networkx as nx

NUMPAD = nx.DiGraph()

N = -1j
S = 1j
W = -1
E = 1
D_TO_LBL = {N: '^', S: 'v', E: '>', W: '<'}
LBL_TO_D = {v: k for k, v in D_TO_LBL.items()}

FOURDIRS = [N, S, E, W]
numpadstr = '''789
456
123
 0A'''

from utils import *
co_to_c, _, _ = parse_complex(numpadstr)

for co in co_to_c:
    for d in FOURDIRS:
        if co + d in co_to_c and co_to_c[co] != ' ' and co_to_c[co + d] != ' ':
            NUMPAD.add_edge(co_to_c[co], co_to_c[co + d], label = D_TO_LBL[d])

dirpadstr = ''' ^A
<v>'''

from utils import *
co_to_c, _, _ = parse_complex(dirpadstr)
DIRPAD = nx.DiGraph()
for co in co_to_c:
    for d in FOURDIRS:
        if co + d in co_to_c and co_to_c[co] != ' ' and co_to_c[co + d] != ' ':
            DIRPAD.add_edge(co_to_c[co], co_to_c[co + d], label = D_TO_LBL[d])

code = '029A'
def get_presses(code, pad):
    spath = [nx.shortest_path(pad, x1, x2)  for x1, x2 in zip('A' + code, code) ]
    presses_without_A = [[pad.edges[x1, x2]['label'] for x1, x2 in zip(p, p[1:])] for p in spath]
    presses = 'A'.join([''.join(x) for x in presses_without_A]) + 'A'
    return presses
numpad1 = get_presses(code, NUMPAD)
dirpad1 = get_presses(numpad1, DIRPAD)
dirpad2 = get_presses(dirpad1, DIRPAD)
dirpad3 = get_presses(dirpad2, DIRPAD)
len(dirpad3) * int( ''.join([c for c in code if c != 'A' and c != '0']) ) #
pass