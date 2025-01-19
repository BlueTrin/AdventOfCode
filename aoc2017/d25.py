from aoc_lube import fetch
from collections import defaultdict

s = fetch(2017, 25)

# s = '''Begin in state A.
# Perform a diagnostic checksum after 6 steps.
#
# In state A:
#   If the current value is 0:
#     - Write the value 1.
#     - Move one slot to the right.
#     - Continue with state B.
#   If the current value is 1:
#     - Write the value 0.
#     - Move one slot to the left.
#     - Continue with state B.
#
# In state B:
#   If the current value is 0:
#     - Write the value 1.
#     - Move one slot to the left.
#     - Continue with state A.
#   If the current value is 1:
#     - Write the value 1.
#     - Move one slot to the right.
#     - Continue with state A.'''

boot, *states = s.split('\n\n')

start = boot.splitlines()[0].split()[-1][0]
steps = int(boot.splitlines()[1].split()[-2])
print(start, steps)

state_rules = {}
for stateinfo in states:
    state_s, *ruleset = stateinfo.splitlines()
    state = state_s.split()[-1][0]

    val_map = {}
    for rule in [ruleset[i:i+4] for i in range(0, len(ruleset), 4)]:
        val = int(rule[0].replace(':', '').split()[-1])
        write = int(rule[1].replace('.', '').split()[-1])
        move = rule[2].replace('.', '').split()[-1]
        next_state = rule[3].replace('.', '').split()[-1]
        val_map[val] = (write, move, next_state)
    state_rules[state] = val_map

print(state_rules)

tape = defaultdict(int)
state = start
pos = 0

for _ in range(steps):
    val = tape[pos]
    write, move, state = state_rules[state][val]
    tape[pos] = int(write)
    pos += 1 if move == 'right' else -1

print(sum(tape.values()))