from fontTools.afmLib import readlines

q5_inp = '''2 3 4 5
3 4 5 2
4 5 2 3
5 2 3 4'''

from utils import parse_complex
def p1(txt, part):
    res = None
    for i_y, r in enumerate([r for r in txt.splitlines() if r]):
        for i_x, c in enumerate(r.split()):
            if res is None:
                res = [[] for i in  range(len(r.split()))]
            res[i_x].append(int(c))

    next_clap = 0

    turn =0
    shouted = {}
    best_shouted = 0
    while True:
        d = res[next_clap].pop(0)
        new_col = (next_clap + 1) % len(res)

        new_place = (d-1) % len(res[new_col])
        before = ((d-1) // len(res[new_col])) % 2 == 0
        if before:
            res[new_col].insert(new_place, d)
        else:
            res[new_col].insert(len(res[new_col]) - new_place, d)
        # find the position of the next dancer
        shout = ''.join([str(x[0]) for x in res])
        # print(f" --> shout({turn})={shout}")

        if part == 2 or part == 3:
            shouted[shout] = shouted.get(shout, 0) + 1

            if int(shout) > best_shouted:
                best_shouted = int(shout)
            if part == 2 and shouted[shout] >= 2024:
                return int(shout)  *  (turn+1)
        turn += 1
        next_clap = new_col
        if part == 3 and turn %10000000 == 0:
            print(best_shouted)
        if part == 1 and turn >= 10:
            break


    return shout


print(p1(q5_inp, 1))

q5_inp = open("q5_p1.txt").read()
print(p1(q5_inp, 1))

q5_inp = '''2 3 4 5
6 7 8 9'''
print(p1(q5_inp, 2))
q5_inp = open("q5_p2.txt").read()
print(p1(q5_inp, 2))


# q5_inp = '''2 3 4 5
# 6 7 8 9'''
# print(p1(q5_inp, 3))
q5_inp = open("q5_p3.txt").read()
print(p1(q5_inp, 3))
