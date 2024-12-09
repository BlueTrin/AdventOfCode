# runs in 7-8 ms
  
from heapq import heappush, heappop

def can_solve_fast(sol, vals):
    h = []
    heappush(h, (1, sol, vals))
    while h:
        _, tgt, vals = heappop(h)

        if (strtgt:=str(tgt)).endswith(str(vals[-1])): # check if last op can be concatenate
            if len(str(vals[-1])) < len(strtgt):
                next_val = int(strtgt[:-len(str(vals[-1]))])
                if len(vals) == 2:
                    if next_val == vals[0]:
                        return True
                else:
                    heappush(h, (1, next_val, vals[:-1]))   # this is prio1 because concatenation is probably rare

        if tgt % vals[-1] == 0:     # check if last operation was a mult
            next_val = tgt//vals[-1]
            if len(vals) == 2:
                if next_val == vals[0]:
                    return True
            else:
                heappush(h, (2, next_val, vals[:-1]))   # prio 2 because it is relatively rare


        next_val = tgt - vals[-1]       # just consider if last op is +
        if len(vals) == 2:
            if next_val == vals[0]:
                return True
        elif next_val > 0:
            heappush(h, (3, next_val, vals[:-1]))   # this is more or less a catch all

    return False

def part2_fast(txt_inp):
    eq_lst = []
    for r in txt_inp.split("\n"):
        if r:
            sol, rightside = r.split(":")
            sol = int(sol)
            vals = tuple(int(x) for x in rightside.split(" ") if x)
            eq_lst.append((sol, vals))

    total = 0
    for sol, val in eq_lst:
        if can_solve_fast(sol, val):
            total += sol

    return total

if __name__ == '__main__':
    for tgt, vals, exp in [
        (190, (10, 19), True),
        (3267, (81, 40, 27), True),
        (83, (17, 5), False),
        (156, (15, 6),True),
        ]:
        if  can_solve_fast(tgt, vals) != exp:
            raise RuntimeError("ERR")

    txt_inp = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''
    eq_lst = parse_input(txt_inp)
    # print(part1(eq_lst))
    print(part2_fast(txt_inp))


    txt_inp = get_input(7, year=2024)
    # eq_lst = parse_input(txt_inp)
    # print(part1(eq_lst))
    import     time
    start = time.perf_counter()
    print(part2_fast(txt_inp))
    end  = time.perf_counter()
    print(f"Computation time = {1000 * (end - start):.3f}ms")

