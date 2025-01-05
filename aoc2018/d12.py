from aoc_lube import fetch

s = fetch(2018, 12)
t = '''initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #'''

initial_s, rules_s = s.split('\n\n')

initial = initial_s.split(': ')[1]
rules = { r.split(' => ')[0]: r.split(' => ')[1] for r in rules_s.splitlines() }
print(initial, rules)

def next_gen(state, rules, start):
    new_state = ""
    for i in range(0, 2+len(state)+2):
        curr_patt = (".." + state + "..")[i-2:i+3]
        new_state += rules.get(curr_patt, ".")
    return new_state, start-2

init_len = len(initial)
shift = 0
print(0, initial)
for i in range(20):
    initial, shift = next_gen(initial, rules, shift)
    print(i+1, initial)

print(sum([i+shift for i, c in enumerate(initial) if c == '#']))

# 2178 too low
# 3494 too high