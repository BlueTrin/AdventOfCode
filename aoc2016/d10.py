from aoc_lube import fetch
from collections import defaultdict


s = fetch(2016, 10)

bots = defaultdict(list)
output = defaultdict(list)
instr = defaultdict(dict)
for r in s.splitlines():
    if not r:
        continue
    if r.startswith("value "):
        _, v1, _, _, _, v2 = r.split()
        bots[v2].append(int(v1))

    if r.startswith("bot "):
        _, b, _, _, _, ltype, l, _, _, _, htype, h = r.split()
        instr[b] = {"l": (ltype, l), "h": (htype, h)}

has_switch = True
while has_switch:
    has_switch = False
    bots_lst = list(bots.keys())
    for k in bots_lst:
        if len(bots[k]) == 2:
            lv, hv = sorted(bots[k])
            if lv == 17 and hv == 61:
                print("Part 1:", k)
            if lb:=instr.get(k, {}).get("l"):
                if lb[0] == "bot":
                    bots[lb[1]].append(lv)
                else:
                    output[lb[1]].append(lv)
            if hb:=instr.get(k, {}).get("h"):
                if hb[0] == "bot":
                    bots[hb[1]].append(hv)
                else:
                    output[hb[1]].append(hv)
            bots[k] = []
            instr.pop(k)
            has_switch = True


print("Part 2:", output["0"][0] * output["1"][0] * output["2"][0])
# 5035 too low
pass