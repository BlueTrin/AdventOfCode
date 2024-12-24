from functools import cache
from typing import Set
from collections.abc import Iterable
from collections import deque
import itertools
import copy


reg = {}
instr = {}


@cache
def solve_rec(rres):
    if rres in reg:
        res = reg[rres]
    else:
        r1, op, r2 = instr[rres]
        r1 = solve_rec(r1)
        r2 = solve_rec(r2)
        if op == "OR":
            res = r1 | r2
        elif op == "XOR":
            res = r1 ^ r2
        elif op == "AND":
            res = r1 & r2
        else:
            raise RuntimeError("dur dur")
    # print(f"{rres}={res}")
    return res


def readinp(inp):
    global reg, instr
    init_vals_str, instr_str = inp.split("\n\n")

    for r in init_vals_str.splitlines():
        x, y = r.split(": ")
        reg[x] = int(y)

    for r in instr_str.splitlines():
        r1, op, r2, _assign, rres = r.split(" ")
        instr[rres] = (r1, op, r2)
    return reg, instr


def gettotal(initial):
    solr = [solve_rec(r) for r in
            sorted(set(rin for rin in
                       list(instr.keys()) + list(reg.keys())
                       if rin.startswith(initial)))]
    return int(''.join(reversed([str(x) for x in solr])), 2)


def part1(inp):
    global reg, instr
    readinp(inp)
    solve_rec.cache_clear()

    return gettotal("z")


def get_nodes(roots, depth) -> Set[str]:
    if not isinstance(roots, str) and isinstance(roots, Iterable):
        return set.union(*[get_nodes(n, depth) for n in roots])

    if depth == 0:
        return set([roots])
    else:
        ret = set()
        if roots in instr:
            ret |= (set([roots]) | get_nodes(instr[roots][0], depth-1)
                    | get_nodes(instr[roots][2], depth-1))

        for n, n_calc in instr.items():
            if roots in [n_calc[0], n_calc[2]]:
                ret |= get_nodes(n, depth-1)
        return ret


def find_error_pos(val_sw):
    global instr
    orig_instr = copy.copy(instr)
    
    for sw_it1, sw_it2 in val_sw:
        instr[sw_it1], instr[sw_it2] = instr[sw_it2], instr[sw_it1]

    solve_rec.cache_clear()

    try:
        real_res = gettotal("x") + gettotal("y")
        bad_res = gettotal("z")
    except RecursionError:
        # ZOMG everything is broken
        return 0
    finally:
        instr = copy.copy(orig_instr)
        solve_rec.cache_clear()
    
    # print(f"{real_res} != {bad_res}")
    for ic, c in enumerate(reversed(bin(bad_res ^ real_res))):
        if c == '1':
            return ic
    return None


def part2(inp):
    global instr
    readinp(inp)

    q = deque([[]])
    while q:
        val_sw = q.pop()
        if (next_err:=find_error_pos(val_sw)) is None:
            return val_sw  # defensive peogramming will not be hit
        if len(val_sw) >= 4:
            continue
        
        candidates = get_nodes({f"z{next_err:02d}", f"x{next_err:02d}", f"y{next_err:02d}"}, 2)

        for sw1, sw2 in itertools.combinations(candidates, 2):
            if sw1 not in instr or sw2 not in instr:
                continue
            if sw1 in val_sw or sw2 in val_sw:
                continue
            cand_error_pos = find_error_pos(val_sw + [(sw1, sw2)])

            if cand_error_pos is None:
                return ",".join(sorted(itertools.chain(*(val_sw + [(sw1, sw2)]))))
            elif cand_error_pos > next_err:
                q.append(val_sw + [(sw1, sw2)])
                print(f" -> switch {sw1} and {sw2} improved from {next_err} {cand_error_pos} -> {val_sw}")
                continue
    raise RuntimeError(f"failed to solve candidates={candidates}")


assert(part1("""x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
""")) == 4

print(part1(open("2024_24.txt").read()),
      file=open("24sol.txt", "w"))

print(part2(open("2024_24.txt").read()))
