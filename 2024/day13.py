inp = '''Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279'''

from aoc_input import get_input
inp = get_input(13,2024)
# inp = open("day13_input.txt").read()

p_lst = []
for x in inp.split("\n\n"):
    ba, bb, p = x.splitlines()
    xa,ya = [int(x.split(",")[0]) for x in ba.split("+")[1:]]

    xb,yb = [int(x.split(",")[0]) for x in bb.split("+")[1:]]
    xp,yp = [int(x.split(",")[0]) for x in p.split("=")[1:]]
    p_lst.append((xa, ya, xb, yb, 10000000000000+xp, 10000000000000+yp))

from z3 import Int, Optimize, And, sat
total= 0
for xa, ya, xb, yb, xp, yp in p_lst:
    # for pa in range(101):
    #     for pb in range(101):
    #         if xa * pa + xb * pb == xp and ya * pa + yb * pb == yp:
    #             print(pa, pb)
    pa = Int('pa')
    pb = Int('pb')
    cost = Int('cost')
    opt = Optimize()
    opt.add(And(pa >0, pb>0, xa*pa + xb*pb == xp, ya*pa + yb * pb == yp))
    opt.add(cost == pa*3 + pb)
    h = opt.minimize(cost)
    print(opt.check())
    print(opt.lower(h))
    print(opt.model())
    if opt.check() == sat:
        total += opt.lower(h).as_long()

print(total)
