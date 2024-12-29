import itertools

from aoc_lube import fetch

s = fetch(2015, 21)
boos_hp = int(s.splitlines()[0].split()[-1])
boss_attack = int(s.splitlines()[1].split()[-1])
boss_armor = int(s.splitlines()[2].split()[-1])

player_hp = 100

eqp_s = '''Weapons:    Cost  Damage  Armor
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0

Armor:      Cost  Damage  Armor
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5

Rings:      Cost  Damage  Armor
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3'''

weapons = []
for r in eqp_s.split('\n\n')[0].splitlines()[1:]:
    t = r.split()
    weapons.append((int(t[1]), int(t[2]), int(t[3])))

armors = []
for r in eqp_s.split('\n\n')[1].splitlines()[1:]:
    t = r.split()
    armors.append((int(t[1]), int(t[2]), int(t[3])))

rings = []
for r in eqp_s.split('\n\n')[2].splitlines()[1:]:
    t = r.split()
    rings.append((int(t[2]), int(t[3]), int(t[4])))

choices = itertools.product(
    range(len(weapons)),
    range(-1, len(armors)),
    range(-1, len(rings)),
    range(-1, len(rings)))

min_cost = 999999999999
max_cost = 0
for purch in choices:
    cost, atk, arm = weapons[purch[0]]
    if purch[1] != -1:
        cost += armors[purch[1]][0]
        atk += armors[purch[1]][1]
        arm += armors[purch[1]][2]
    if purch[2] != -1:
        cost += rings[purch[2]][0]
        atk += rings[purch[2]][1]
        arm += rings[purch[2]][2]
    if purch[3] != -1:
        cost += rings[purch[3]][0]
        atk += rings[purch[3]][1]
        arm += rings[purch[3]][2]

    if boos_hp // max(1,(atk - boss_armor)) + ( 1 if boos_hp % max(1,(atk - boss_armor)) != 0 else 0) <= (player_hp // max(1, (boss_attack - arm)) + (1 if player_hp % max(1, (boss_attack - arm)) != 0 else 0)):
        if cost < min_cost:
            min_cost = cost
    else:
        if cost > max_cost:
            max_cost = cost

print(min_cost)
print(max_cost)
# Hit Points: 104
# Damage: 8
# Armor: 1