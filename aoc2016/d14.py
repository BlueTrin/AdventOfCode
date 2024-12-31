from aoc_lube import fetch
from hashlib import md5
import re
from collections import defaultdict

s = fetch(2016, 14)

print(s)

def find64(s, stretch=1):
    triplet = defaultdict(set)
    fivlet = defaultdict(set)
    valid = set()
    curr = 0
    while True:
        text = f"{s}{curr}"
        for i in range(stretch):
            m = md5()
            m.update(text.encode('UTF-8'))
            hash = m.hexdigest()
            text = hash

        m = re.search(r"(.)\1\1", hash)
        if m:
            triplet[m.groups()[0]].add(curr)
#        for m in re.finditer(r"(.)\1\1\1\1", hash):
        m = re.search(r"(.)\1\1\1\1", hash)
        if m:
            fivlet[m.groups()[0]].add(curr)
            for t in triplet[m.groups()[0]]:
                if curr in range(t+1, t+1001):
                    valid.add(t)

            if len(valid) >= 64 and curr > sorted(valid)[63] + 1000:
                return sorted(valid)[63]
        curr += 1

print(find64("abc"))
print(find64(s))

print(find64("abc", 2017))
print(find64(s, 2017))

# 27995 too high
# 20219 too high
