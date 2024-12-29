from os import WCONTINUED

from aoc_lube import fetch

s = fetch(2015, 22)
boss_hp = int(s.splitlines()[0].split()[-1])
boss_dmg = int(s.splitlines()[1].split()[-1])
p_hp = 50
p_mana = 500


def play_rec(p_hp, p_mana, b_hp, b_dmg, shield, poison, recharge, p_turn, p_mana_spent, p_mana_spent_min, hard, seq=None):
    """
    Magic Missile costs 53 mana. It instantly does 4 damage.
    Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
    Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
    Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
    Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.
    """
    if seq[:3] == ['Poison', 'Recharge', 'Shield', ]:
        pass
    if seq[:6] == ['Poison', 'Recharge', 'Shield', 'Poison', 'Recharge', 'Drain', ]:
        pass
    if seq[:7] == ['Poison', 'Recharge', 'Shield', 'Poison', 'Recharge', 'Drain', 'Poison']:
        pass
    if seq[:10] == (['Poison', 'Recharge', 'Shield', 'Poison', 'Recharge', 'Drain', 'Poison',]\
            + ["Magic Missile"]*3):
        pass
    if seq[:19] == (['Poison', 'Recharge', 'Shield', 'Poison', 'Recharge', 'Drain', 'Poison',]\
            + ["Magic Missile"]*12):
        pass

    if seq is None:
        seq = []
    if p_turn and hard:
        p_hp -= 1
        if p_hp <= 0:
            return p_mana_spent_min

    if p_mana_spent >= p_mana_spent_min:
        return p_mana_spent_min

    if recharge:
        p_mana += 101
        recharge -= 1
    if poison:
        b_hp -= 3
        poison -= 1
    if shield:
        armor = 7
        shield -= 1
    else:
        armor = 0

    if b_hp <= 0:
        return p_mana_spent

    if p_turn:
        if p_mana >= 173 and poison == 0:
            p_mana_spent_min = min(p_mana_spent_min, play_rec(p_hp, p_mana-173, b_hp, b_dmg, shield, 6, recharge, not p_turn, p_mana_spent+173, p_mana_spent_min, hard, seq+["Poison"]))
        if p_mana >= 53:
            p_mana_spent_min = min(p_mana_spent_min,
                                   play_rec(
                                       p_hp, p_mana-53, b_hp-4, b_dmg, shield, poison, recharge, not p_turn, p_mana_spent+53, p_mana_spent_min, hard, seq+["Magic Missile"]))

        if p_mana >= 73:
            p_mana_spent_min = min(p_mana_spent_min, play_rec(p_hp+2, p_mana-73, b_hp-2, b_dmg, shield, poison, recharge, not p_turn, p_mana_spent+73, p_mana_spent_min, hard, seq+["Drain"]))
        if p_mana >= 113 and shield == 0:
            p_mana_spent_min = min(p_mana_spent_min, play_rec(p_hp, p_mana-113, b_hp, b_dmg, 6, poison, recharge, not p_turn, p_mana_spent+113, p_mana_spent_min, hard, seq+["Shield"]))
        if p_mana >= 229 and recharge == 0:
            p_mana_spent_min = min(p_mana_spent_min, play_rec(p_hp, p_mana-229, b_hp, b_dmg, shield, poison, 5, not p_turn, p_mana_spent+229, p_mana_spent_min, hard, seq+["Recharge"]))
        return p_mana_spent_min
    else:
        p_hp -= max(b_dmg - armor, 1)
        if p_hp <= 0:
            return p_mana_spent_min

        return min(p_mana_spent_min, play_rec(p_hp, p_mana, b_hp, b_dmg, shield, poison, recharge, not p_turn, p_mana_spent, p_mana_spent_min, hard, seq))

#print(play_rec(p_hp, p_mana, boss_hp, boss_dmg, 0, 0, 0, True, 0, 99999999999, False, seq=[]))
print(play_rec(p_hp, p_mana, boss_hp, boss_dmg, 0, 0, 0, True, 0, 99999999999, hard=True, seq=[]))
# 1242 too high
# 1013 too low