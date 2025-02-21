from aoc_lube import fetch
import typing as t
import logging
import enum
import itertools

logging.basicConfig()
logger = logging.getLogger(__name__)


class Tree(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        if self.value is not None:
            assert self.left is None and self.right is None
            return f"{self.value}"
        else:
            assert self.left is not None and self.right is not None
            return f"[{self.left},{self.right}]"

    def __repr__(self):
        if self.value is not None:
            assert self.left is None and self.right is None
            return f"{self.value}"
        else:
            assert self.left is not None and self.right is not None
            return f"[{self.left},{self.right}]"

    def set_left(self, left):
        self.left = left
        left.parent = self

    def set_right(self, right):
        self.right = right
        right.parent = self


s = fetch(2021, 18)


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

        parent = Tree(None)
        parent.set_left(read_tuple(r[:i_s]))
        parent.set_right(read_tuple(r[i_s+1:]))
        return parent

    else:
        return Tree(int(r))


class SearchType(enum.Enum):
    LEVEL = enum.auto()
    EXPLODE = enum.auto()


def find_first_action(t: Tree, search_type: SearchType, level=0) -> t.Optional[Tree]:
    if search_type == SearchType.EXPLODE and t.value is not None and t.value >= 10:
        return t

    if search_type == SearchType.LEVEL and level >= 4 and t.left is not None and t.right is not None:
        assert t.left.value is not None and t.right.value is not None
        return t

    if t.left is not None:
        left_first_action = find_first_action(t.left, search_type, level + 1)
        if left_first_action is not None:
            return left_first_action

    if t.right is not None:
        right_first_action = find_first_action(t.right, search_type, level + 1)
        if right_first_action is not None:
            return right_first_action

    return None

def reduce_tree(t: Tree) -> Tree:
    while reduce_first_action(t):
        pass
    return t

def reduce_first_action(t: Tree) -> bool:
    c = find_first_action(t, SearchType.LEVEL)
    if c is None:
        c = find_first_action(t, SearchType.EXPLODE)

    if c is None:
        return False
    elif c.value is not None and c.value >= 10:
        logger.debug(f"  ** SPLITTING {c}")
        # To split a regular number, replace it with a pair; the left element of the pair should be the regular number
        # divided by two and rounded down, while the right element of the pair should be the regular number divided by
        # two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
        c.set_left(Tree(c.value // 2))
        c.set_right(Tree(c.value - (c.value // 2)))
        c.value = None
        logger.debug(f"  -> {t}\n")
        return True
    else:
        logger.debug(f"  ** EXPLODING {c}")

        # If any pair is nested inside four pairs, the leftmost such pair explodes.
        # To explode a pair, the pair's left value is added to the first regular number to the left of the exploding
        # pair (if any), and the pair's right value is added to the first regular number to the right of the exploding
        # pair (if any). Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is
        # replaced with the regular number 0.
        assert c.left is not None and c.right is not None
        assert c.left.value is not None and c.right.value is not None
        lval, rval = c.left.value, c.right.value
        c.left = None
        c.right = None
        c.value = 0

        curr_it = c
        while True:
            parent = curr_it.parent
            if parent is None:
                break
            if parent.left == curr_it:
                curr_it = parent
                continue
            if parent.right == curr_it:
                child_left = parent.left
                while child_left.value is None:
                    child_left = child_left.right
                child_left.value += lval
                break

        curr_it = c
        while True:
            parent = curr_it.parent
            if parent is None:
                break
            if parent.right == curr_it:
                curr_it = parent
                continue
            if parent.left == curr_it:
                child_right = parent.right
                while child_right.value is None:
                    child_right = child_right.left
                child_right.value += rval
                break

        logger.debug(f"  -> {t}\n")
        return True

def magnitude(t: Tree) -> int:
    # To check whether it's the right answer, the snailfish teacher only checks the magnitude of the final sum.
    # The magnitude of a pair is 3 times the magnitude of its left element plus 2 times the magnitude of its right
    # element. The magnitude of a regular number is just that number.
    if t.value is not None:
        return t.value
    else:
        assert t.left is not None and t.right is not None
        return 3* magnitude(t.left) + 2*magnitude(t.right)

# a few test cases
t = read_tuple("[[[[[9,8],1],2],3],4]")
reduce_tree(t)
assert str(t) == '[[[[0,9],2],3],4]'

t = read_tuple("[7,[6,[5,[4,[3,2]]]]]")
reduce_tree(t)
assert str(t) == '[7,[6,[5,[7,0]]]]'

t = read_tuple("[[6,[5,[4,[3,2]]]],1]")
reduce_tree(t)
assert str(t) == '[[6,[5,[7,0]]],3]'

t = read_tuple("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
reduce_tree(t)
assert str(t) == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'

t = read_tuple("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
reduce_tree(t)
assert str(t) == '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'

# magnitude test cases
assert magnitude(read_tuple("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]")) == 3488

def process_math_homework(s, debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    res = None
    for r in s.splitlines():
        if res is None:
            res = read_tuple(r)
        else:
            new_res = Tree(None)
            new_res.set_left(res)
            right_elt = read_tuple(r)
            new_res.set_right(right_elt)

            logger.debug(f"  {res}")
            logger.debug(f"+ {right_elt}")
            res = new_res
            reduce_tree(res)
            logger.debug(f"= {res}\n")
    logger.debug(f"--------------------------------\n")
    return res

t = process_math_homework('''[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]''', debug=True)
assert str(t) == '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'

t = process_math_homework('''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]''', debug=True)
assert str(t) == '[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]'

t = process_math_homework('''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]''', debug=True)
assert str(t) == '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'

t = process_math_homework('''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]''')
assert magnitude(t) == 4140

print(f"Part1: {magnitude(process_math_homework(s))}")
# 3938 too low

def process_math_homework2(s, debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    res = 0
    rows = s.splitlines()
    for sn1, sn2 in itertools.permutations(rows, 2):
        sn = Tree(None)
        sn.set_left(read_tuple(sn1))
        sn.set_right(read_tuple(sn2))
        reduce_tree(sn)

        res = max(res, magnitude(sn))
    return res

print(f"Part2: {process_math_homework2(s)}")
