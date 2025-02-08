from aoc_lube import fetch

from collections import defaultdict

s = fetch(2021, 3)


def solve(s):
    counter = defaultdict(int)
    for r in s.splitlines():
        for i, c in enumerate(r):
            if c == '1':
                counter[i] += 1

    # Each bit in the gamma rate can be determined by finding the most common bit in the corresponding position of all
    # numbers in the diagnostic report.
    gamma_rate = int(''.join(['1' if counter[i] >= (len(s.splitlines())/2) else '0' for i in range(len(counter))]), 2)

    # The epsilon rate is calculated in a similar way; rather than use the most common bit, the least common bit from each
    # position is used.
    epsilon_rate = int(''.join(['1' if counter[i] < (len(s.splitlines())/2) else '0' for i in range(len(counter))]), 2)

    # The power consumption can then be found by multiplying the gamma rate by the epsilon rate.

    o2_candidates = [r for r in s.splitlines()]
    for i in range(len(r)):
        count1 = sum([1 for r in o2_candidates if r[i] == '1'])
        b = '1' if count1 >= (len(o2_candidates)/2) else '0'
        o2_candidates = [r for r in o2_candidates if r[i] == b]
        if len(o2_candidates) == 1:
            break

    co2_candidates = [r for r in s.splitlines()]
    for i in range(len(r)):
        count1 = sum([1 for r in co2_candidates if r[i] == '1'])
        b = '0' if count1 >= (len(co2_candidates)/2) else '1'
        co2_candidates = [r for r in co2_candidates if r[i] == b]
        if len(co2_candidates) == 1:
            break

    #Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating,
    # then multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in
    # decimal, not binary.)
    return gamma_rate, epsilon_rate, int(o2_candidates[0], 2), int(co2_candidates[0], 2)
    # 2974222 too low

gamma_rate, epsilon_rate, o2, co2 = solve('''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010''')
print(f"Part1: {gamma_rate * epsilon_rate}")
print(f"Part2: {o2 * co2}")


gamma_rate, epsilon_rate, o2, co2 = solve(s)
assert gamma_rate * epsilon_rate == 2972336
print(f"Part1: {gamma_rate * epsilon_rate}")
print(f"Part2: {o2 * co2}")
