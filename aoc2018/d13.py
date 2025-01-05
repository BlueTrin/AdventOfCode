from aoc_lube import fetch

from utils.utils import Point

s = fetch(2018, 13)
# s = r'''/->-\
# |   |  /----\
# | /-+--+-\  |
# | | |  | v  |
# \-+-/  \-+--/
#   \------/  '''

# s = r'''/>-<\
# |   |
# | /<+-\
# | | | v
# \>+</ |
#   |   ^
#   \<->/'''
N = -1j
S = 1j
W = -1
E = 1

FOURDIRS = [N, S, E, W]

ARROWDIR = {
    '^': N,
    'v': S,
    '<': W,
    '>': E
}
ARROW2TRACK = {
    '^': '|',
    'v': '|',
    '<': '-',
    '>': '-'
}

NEWDIR = {
    ('/', N): E,
    ('/', S): W,
    ('/', E): N,
    ('/', W): S,
    ('\\', N): W,
    ('\\', S): E,
    ('\\', E): S,
    ('\\', W): N,
    ('+', N): (W, N, E),
    ('+', S): (E, S, W),
    ('+', E): (N, E, S),
    ('+', W): (S, W, N),
    ('|', N): N,
    ('|', S): S,
    ('-', E): E,
    ('-', W): W
}

carts = []
tracks = {}
for y, r in enumerate(s.splitlines()):
    for x, c in enumerate(r):
        if c == ' ':
            continue
        if c in ARROWDIR:
            carts.append((x + 1j* y, ARROWDIR[c], 0))
            c = ARROW2TRACK[c]
        tracks[x+ 1j*y] = c

while True:
    carts.sort(key=lambda x: (x[0].imag, x[0].real))
    crashed_carts = set()
    print(carts)
    if len(carts) == 1:
        last_round = True
    else:
        last_round = False

    for i in range(len(carts)):
        pt, d, t = carts[i]
        if pt in crashed_carts:
            continue

        new_pt = pt + d
        new_d = NEWDIR[(tracks[new_pt],d)]
        if isinstance(new_d, tuple):
            new_d = new_d[t]
            t = (t+1)%3
        carts[i] = (new_pt, new_d, t)
        for j, (pt2, _, _) in enumerate(carts):
            if i == j:
                continue
            if pt2 == new_pt:
                crashed_carts.add(pt)
                crashed_carts.add(pt2)
                print("crash", new_pt)
                break
    carts = [x for x in carts if x[0] not in crashed_carts]
    if len(carts) == 1:
        print(carts)
        break
    if last_round:
        print(carts)
        #124,91 = wrong
        break