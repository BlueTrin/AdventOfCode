from aoc_lube import fetch
import typing as t
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)


s = fetch(2021, 18)

print(s)

def read_tuple(r):
    if r[0] == '[':
        assert r[-1] == ']'
        r = r[1:-1]
        brackets = 0
        i_s = 0
        while brackets > 0 or r[i_s] != ',':
            if r[i_s] == '[':
                brackets += 1
            elif r[i_s] == ']':
                brackets -= 1
            i_s += 1
        assert r[i_s] == ','
        sub_elt1 = read_tuple(r[:i_s])
        sub_elt2 = read_tuple(r[i_s+1:])
        return sub_elt1, sub_elt2

    else:
        return int(r)

def pass_vright(sn, vright):
    if vright is None:
        return sn
    elif isinstance(sn, int):
        return sn + vright
    else:
        return pass_vright(sn[0], vright), sn[1]

def reduce_sn(sn, level=0):
    stop_actions, sn, _, _ = reduce_sn_impl(sn, level=0)
    return stop_actions, sn

def reduce_sn_impl(sn, level=0, left_explode=None) -> t.Tuple[bool, t.Union[int, t.Tuple], t.Optional[int], t.Optional[int]]:
    if isinstance(sn, int):
        if left_explode:
            sn += left_explode
        if sn >= 10:
            # if number is too big then it is split in a tuple
            return True, (sn//2, sn - sn//2), None, None
        else:
            # otherwise we just return the element
            return False, sn, None, None
    elif isinstance(sn, tuple):
        if level >= 4:
            # over level 4 we just explode, this leaves 0 where the tuple was
            return True, 0, sn[0], sn[1]
        else:
            stop_actions, val_l, vleft, vright = reduce_sn_impl(sn[0], level+1)

            if stop_actions:
                if isinstance(sn[1], int) and vright is not None:
                    return True, (val_l, sn[1] + vright), vleft, None
                else:
                    # PASS VRIGHT SN[1]
                    return True, (val_l, pass_vright(sn[1], vright)), vleft, None

            # we check if we have actions on the right side
            assert not stop_actions
            stop_actions, val_r, vleft, vright = reduce_sn_impl(sn[1], level+1, vright)
            if stop_actions:
                if isinstance(val_l, int) and vleft is not None:
                    return True, (val_l + vleft, val_r), None, vright
                else:
                    return True, (val_l, val_r), vleft, vright
            # if we have no actions on the right side we just return the sum of the two sides
            assert not stop_actions
            return False, (val_l, val_r), None, None
    else:
        raise RuntimeError(f"Invalid sn {sn}")

def solve(s, debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    res = None
    for row in s.splitlines():
        r = read_tuple(row)
        if res is None:
            res = r
        else:
            res = res, r

        while True:
            stop_action, res = reduce_sn(res)
            if not stop_action:
                break

        logger.debug(f"res={res}")
    return res

t = read_tuple('[[[[4,3],4],4],[7,[[8,4],9]]]'), read_tuple('[1,1]')
_, t = reduce_sn(t)
_, t = reduce_sn(t)
_, t = reduce_sn(t)
_, t = reduce_sn(t)
_, t = reduce_sn(t)
assert t == ((((0,7),4),((7,8),(6,0))),(8,1))

t = solve('''[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]''')
assert t == ((((5, 0), (7, 4)), (5, 5)), (6, 6))


t = solve('''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]''', debug=True)

def magnitude(p):
    if isinstance(p, int):
        return p
    else:
        return 3*magnitude(p[0]) + 2*magnitude(p[1])

res  = solve(s)
print(magnitude(res))
# 1766 too low
pass
