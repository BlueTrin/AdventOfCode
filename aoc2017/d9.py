from aoc_lube import fetch

s = fetch(2017, 9)

class Tree(object):
    def __init__(self, parent=None):
        self.children = []
        self.garbage = []
        if parent is None:
            self.score = 1
        else:
            self.parent = parent
            self.score = parent.score + 1

    def __repr__(self):
        return f"Tree(children={self.children}, garbage={self.garbage})"

def resolve(s):
    score = 0
    non_cancelled = 0
    assert s[0] == '{'
    assert s[-1] == '}'
    s = s[1:-1]

    curr = Tree()
    score += curr.score

    while s:
        if s[0] == '{':
            c = Tree(curr)
            score += c.score
            curr.children.append(c)
            curr = c
            s = s[1:]
        elif s[0] == '<':
            garb_it = 1
            cancelled = 0
            while s[garb_it] != '>':
                if s[garb_it] == '!':
                    garb_it += 2
                    cancelled += 2
                else:
                    garb_it += 1
            curr.garbage.append(s[1:garb_it])
            non_cancelled += garb_it - 1 - cancelled
            s = s[garb_it+1:]
        elif s[0] == ',':
            s = s[1:]
        elif s[0] == '}':
            if curr.parent:
                curr = curr.parent
                s = s[1:]
            else:
                break
        else:
            raise RuntimeError(f"Unexpected: {s}")

    return curr, score, non_cancelled


parent, score, non_cancelled = resolve(s)
print(f"Part1: {score}")
print(f"Part2: {non_cancelled}")

pass
