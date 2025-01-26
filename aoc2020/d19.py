import more_itertools
from aoc_lube import fetch
from collections import deque
from pprint import pp
s = fetch(2020, 19)


def read_input(s, p2=False):
    rules, messages = s.split('\n\n')
    ruleset = {}
    for row in rules.splitlines():
        if p2 and row.startswith('8:'):
            row = '''8: 42 | 42 8'''
        elif p2 and row.startswith('11:'):
            row = '''11: 42 31 | 42 11 31'''
        r, v = row.replace('"', '').split(': ')
        ruleset[r] = tuple(tuple(x.split()) for x in v.split(' | '))

    # simplify rules - DOES NOT WORK
    single_ruleset = [k for k, v in ruleset.items() if len(v) == 1 and k != '0']

    has_simplified = True
    while has_simplified:
        has_simplified = False
        for k, v_t in ruleset.items():
            new_vt = tuple()
            for v in v_t:
                new_v = v
                for sr in single_ruleset:
                    new_v = tuple(more_itertools.collapse(tuple(x if x != sr else ruleset[sr][0] for x in new_v)))
                if new_v != v:
                    has_simplified = True
                new_vt += (new_v, )
            ruleset[k] = new_vt

    for sr in single_ruleset:
        del ruleset[sr]

    ruleset = {k: ruleset[k] for k in sorted(ruleset.keys(), key=lambda x: int(x))}

    return ruleset, messages

def check_msg(ruleset, r, debug=False):
    orig = r
    d = deque([(r, ('0', ), tuple())])
    while d:
        m, r_lst, history = d.popleft()

        wrong_match = False
        while r_lst and r_lst[0] in 'ab':
            if m.startswith(r_lst[0]):
                m = m[1:]
                r_lst = r_lst[1:]
            else:
                wrong_match = True
                break

        if wrong_match:
            continue

        if not r_lst:
            if not m:
                return True
            continue

        for r in ruleset[r_lst[0]]:
            expanded_rule = r + r_lst[1:]
            if len(expanded_rule) > len(m):
                continue
            if r[0] not in 'ab' or r[0] == m[0]:
                d.append((m, expanded_rule, history + ((r_lst[0], r),)))

    return False

# matches = 0
# ruleset, _ = read_input('''0: 4 1 5
# 1: 2 3 | 3 2
# 2: 4 4 | 5 5
# 3: 4 5 | 5 4
# 4: "a"
# 5: "b"
#
# ababbb
# bababa
# abbbab
# aaabbb
# aaaabbb''')
# # In the above example, ababbb and abbbab match, but bababa, aaabbb, and aaaabbb do not, producing the answer 2.
# assert check_msg(ruleset, 'ababbb')
# assert check_msg(ruleset, 'abbbab')
# assert not check_msg(ruleset, 'bababa')
# assert not check_msg(ruleset, 'aaabbb')
# assert not check_msg(ruleset, 'aaaabbb')
#
# ruleset, messages = read_input(s)
#
# matches = 0
# for r in messages.splitlines():
#     if check_msg(ruleset, r):
#         matches += 1
# assert matches == 113
# print(f"Part1: {matches}")
#

# EXAMPLE PART 2
testp2 = '''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'''
ruleset, messages = read_input(testp2, p2=True)
pp(ruleset)
# babbb  -> 42
# baabb  -> 42
# bbbab  -> 42
# bbbbb  -> 42
# aabaa  -> 31
# abaaa  -> 31

for m in messages.splitlines():
    if m in '''bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
'''.splitlines():
        assert check_msg(ruleset, m)
    else:
        assert not check_msg(ruleset, m)


ruleset, messages = read_input(s, p2=True)
matches = 0
for r in messages.splitlines():
    if check_msg(ruleset, r):
        matches += 1
print(f"Part2: {matches}")
# 198 too low
