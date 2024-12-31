from aoc_lube import fetch
from collections import deque
from hashlib import md5
from utils.utils import Point

s = fetch(2016, 17)

print(s)


dirs = {'U': Point(0, -1),
        'D': Point(0, 1),
        'L': Point(-1, 0),
        'R': Point(1, 0),
        }

def find_path(s, part2 = False):
    longest_path = ""
    d = deque([(Point(0, 0), '')])
    while d:
        pt, path = d.popleft()
        if pt == Point(3, 3):
            if part2:
                if len(path) > len(longest_path):
                    longest_path = path
                    print(longest_path)
                continue
            else:
                return path
        for (l, di), h in zip(dirs.items(), [c in 'bcdef' for c in md5((s + path).encode()).hexdigest()[:4]]):
            new_pt = pt + di
            if new_pt.x < 0 or new_pt.y < 0 or new_pt.x > 3 or new_pt.y > 3:
                continue
            if not h:
                continue
            if new_pt == Point(3, 3):
                if part2:
                    if len(path+l) > len(longest_path):
                        longest_path = path+l
                        print(longest_path)
                else:
                    return path+l
            else:
                d.append((new_pt, path + l))

    return longest_path


print(find_path("ihgpwlah"))

print(find_path(s))
print(len(find_path(s, True)))