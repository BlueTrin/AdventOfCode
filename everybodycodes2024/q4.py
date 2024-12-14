

q4_inp = '''3
4
7
8'''

def p1(txt):
    i_lst = [int(x) for x in txt.splitlines() if x]
    strikes = sum([x - min(i_lst) for x in i_lst])
    return strikes

print(p1(q4_inp))

q4_inp = open("q4_p1.txt").read()
print(p1(q4_inp))

q4_inp = open("q4_p2.txt").read()
print(p1(q4_inp))

def p3(txt):
    i_lst = [int(x) for x in txt.splitlines() if x]
    import numpy as np
    m = np.median(i_lst)
    strikes = sum([abs(x - m) for x in i_lst])
    return strikes

q4_inp = open("q4_p3.txt").read()
print(p3(q4_inp))