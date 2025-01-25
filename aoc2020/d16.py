from aoc_lube import fetch
import math

s = fetch(2020, 16)
#print(s)

# s = '''class: 1-3 or 5-7
# row: 6-11 or 33-44
# seat: 13-40 or 45-50
#
# your ticket:
# 7,1,14
#
# nearby tickets:
# 7,3,47
# 40,4,50
# 55,2,20
# 38,6,12'''

rule_s, my_ticket_s, ticket_s = s.split('\n\n')

rules = {}
for r in rule_s.splitlines():
    if r.split(': ')[0] in rules:
        raise ValueError(f"Duplicate rule {r.split(': ')[0]}")
    rules[r.split(': ')[0]] = [tuple(map(int, x.split('-'))) for x in r.split(': ')[1].split(' or ')]
print(rules)

nearby = []
for r in ticket_s.splitlines()[1:]:
    nearby.extend(map(int, r.split(',')))
print(nearby)

invalid_nearby = []
for v in nearby:
    for r in rules.values():
        if any(l <= v <= h for l, h in r):
            break
    else:
        invalid_nearby.append(v)

print(f"Part1: {sum(invalid_nearby)}")
# 12044 too low

invalid_nearby = set(invalid_nearby)
nearby_tickets = []
for r in ticket_s.splitlines()[1:]:
    ticket = list(map(int, r.split(',')))
    if any(x in invalid_nearby for x in ticket):
        continue
    nearby_tickets.append(ticket)

values_by_col = {}

for i in range(len(nearby_tickets[0])):
    values_by_col[i] = set(x[i] for x in nearby_tickets)

col_to_rules = {icol: set(rules.keys()) for icol in range(len(nearby_tickets[0]))}

def valid_rule(rule_range, v):
    return any(l <= v <= h for l, h in rule_range)

while True:
    for icol, maybe_rules in col_to_rules.items():
        for rule in list(maybe_rules):
            ranges = rules[rule]
            if all(valid_rule(ranges, v) for v in values_by_col[icol]):
                continue
            maybe_rules.remove(rule)

    if all(len(v) == 1 for v in col_to_rules.values()):
        break

    for icol, maybe_rules in col_to_rules.items():
        if len(maybe_rules) == 1:
            for icol2, maybe_rules2 in col_to_rules.items():
                if icol2 != icol:
                    maybe_rules2 -= maybe_rules

pass
departure_cols = [icol for icol, rules in col_to_rules.items() if any(r.startswith('departure') for r in rules)]

my_ticket = list(map(int, my_ticket_s.splitlines()[1].split(',')))

print(f"Part2: {math.prod(my_ticket[icol] for icol in departure_cols)}")
# 1069784384303