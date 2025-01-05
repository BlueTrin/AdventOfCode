from locale import currency

N = -1j
S = 1j
W = -1
E = 1

NW = N + W
NE = N + E
SW = S + W
SE = S + E
from utils2018 import parse_complex

def print_maze(levels, max_coords ):
    s = ""
    for y in range(int(max_coords[1])):
        for x in range(int(max_coords[0])):
            lvl = [lvl for lvl, pts in levels.items() if x+1j*y in pts][0]
            s += str(lvl)

        s += "\n"
    print(s)

p1_inp = '''..........
..###.##..
...####...
..######..
..######..
...####...
..........'''
def part1(txt, part3=False):
    coord_to_c, c_to_coord, max_coords = parse_complex(txt)

    levels = {0: c_to_coord['.'], 1:c_to_coord['#']}

    if part3:
        DIR_CHECK = [S, E, N, W, NE, NW, SE, SW]
    else:
        DIR_CHECK = [S, E, N, W]
    cur_level = 2
    while True:
        next_pts = set()
        for x in levels[cur_level- 1]:
            if x.real == 0  or x.real == max_coords[0]-1 or x.imag == 0 or x.imag == max_coords[1] -1 :
                continue
            valid = all([x + d not in levels[cur_level- 2] for d in DIR_CHECK])
            if valid:
                next_pts.add(x)
        if not next_pts:
            break
        else:
            levels[cur_level- 1] = levels[cur_level- 1] - next_pts
            levels[cur_level] = next_pts
            cur_level += 1
    if part3:
        print_maze(levels, max_coords)
    return sum(len(s) * lvl for lvl,s in levels.items() if lvl > 0)

print(part1(p1_inp))

p1_inp = open("q4_p1.txt").read()
print(part1(p1_inp))

p1_inp = open("q3_p2.txt").read()
print(part1(p1_inp))


p3_inp = '''..........
..###.##..
...####...
..######..
..######..
...####...
..........'''
print(part1(p3_inp, True))

p3_inp = open("q3_p3.txt").read()
print(part1(p3_inp, True))