from aoc_lube import fetch


val_s = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1'''

valids = {}
for r in val_s.splitlines():
    cat, val = r.split(": ")
    valids[cat] = int(val)


sues = {}
s = fetch(2015, 16)
for r in s.splitlines():
    if not r:
        continue
    sue_s, rest = r.split(": ", 1)
    sue = int(sue_s.split()[1])
    sues[sue] = {(kv:=cat_val.split(": "))[0]: int(kv[1]) for cat_val in rest.split(", ")}

for sue, sue_vals in sues.items():
    if any(valids[sue_att] != sue_val for sue_att, sue_val in sue_vals.items()):
        continue

    print(f"Part 1: {sue}")

for sue, sue_vals in sues.items():
    if any(
            sue_val <= valids[sue_att] if sue_att in ["cats", "trees"]
            else (sue_val >= valids[sue_att] if sue_att in ["pomeranians", "goldfish"]
            else
            valids[sue_att] != sue_val)
           for sue_att, sue_val in sue_vals.items()):
        continue

    print(f"Part 2: {sue}")
