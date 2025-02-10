from aoc_lube import fetch
from itertools import product
from collections import defaultdict

s = fetch(2021, 8)

# s = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
# edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
# fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
# fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
# aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
# fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
# dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
# bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
# egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
# gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'''

ones, fours, sevens, eights = 0, 0, 0, 0
# In the output values, how many times do digits 1, 4, 7, or 8 appear?
for row in s.splitlines():
    l_s, r_s = row.split(' | ')
    l = l_s.split()
    r = r_s.split()

    ones += sum([1 for x in r if len(x) == 2])
    fours += sum([1 for x in r if len(x) == 4])
    sevens += sum([1 for x in r if len(x) == 3])
    eights += sum([1 for x in r if len(x) == 7])
    pass

print(f"Part1: {ones + fours + sevens + eights}")
# 1312 too high

d = {
    '0': {'a', 'b', 'c', 'e', 'f', 'g'},
    '1': {'c', 'f'},
    '2': {'a', 'c', 'd', 'e', 'g'},
    '3': {'a', 'c', 'd', 'f', 'g'},
    '4': {'b', 'c', 'd', 'f'},
    '5': {'a', 'b', 'd', 'f', 'g'},
    '6': {'a', 'b', 'd', 'e', 'f', 'g'},
    '7': {'a', 'c', 'f'},
    '8': {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    '9': {'a', 'b', 'c', 'd', 'f', 'g'}
}

DIG_INTERSECT = defaultdict(lambda: defaultdict(set))

# we do all intersections in advance but store only the number of intersected points
for d1, d2 in product(d.keys(), d.keys()):
    DIG_INTERSECT[d1][len(d[d1] & d[d2])].add(d2)
    DIG_INTERSECT[d2][len(d[d1] & d[d2])].add(d1)

def check_candidates(x, candidates, digit_to_lr):
    final_candidates = []
    xset = set(x)
    # we check against the known digits and intersect with the known table of intersection points
    for known_digit, known_lr in digit_to_lr.items():
        candidates &= DIG_INTERSECT[known_digit][len(set(x) & known_lr)]
        if len(candidates) == 1:
            break

def solve(l, r):
    lr_set = {tuple(sorted(x)) for x in l+r}
    # potential_mappings = {k: {'a', 'b', 'c', 'd', 'e', 'f', 'g'} for k in {'a', 'b', 'c', 'd', 'e', 'f', 'g'}}
    not_found = set(d.keys())
    found = {}
    digit_to_lr = {}

    while not_found:
        has_found = False
        for x in lr_set - found.keys():
            candidates = {k for k in not_found if len(d[k]) == len(x)}
            if len(candidates) > 1 and digit_to_lr:
                check_candidates(x, candidates, digit_to_lr)
            if len(candidates) == 1:
                has_found = True
                k = next(iter(candidates))
                not_found.remove(k)
                found[tuple(x)] = k
                digit_to_lr[k] = set(x)
                # for src in x:
                #     potential_mappings[src] &= d[k]
                #
                # potential_mappings[x] = d[k]
                break
        if not has_found:
            raise RuntimeError("No candidates found")

    return int(''.join([found[tuple(sorted(x))] for x in r]))

p2 = 0
for row in s.splitlines():
    l_s, r_s = row.split(' | ')
    l = l_s.split()
    r = r_s.split()

    p2 += solve(l, r)

print(f"Part2: {p2}")