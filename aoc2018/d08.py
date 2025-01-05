from aoc_lube import fetch
from collections import deque

s = [int(v) for x in fetch(2018, 8).splitlines() if x for v in x.split()]
#s = [int(v) for x in '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'.split() if x for v in x.split()]

q = deque(s)
nodes = {}
curr = 0

def read_rec(q, nodes):
    global curr
    nc = q.popleft()
    nm = q.popleft()
    nodes[curr] = { "children": [], "metadata": [] }
    this = curr
    curr += 1

    for i in range(nc):
        nodes[this]['children'].append(read_rec(q, nodes))

    for i in range(nm):
        nodes[this]['metadata'].append(q.popleft())

    return this

read_rec(q, nodes)

parent = None

for n in nodes:
    is_child = False
    for k in nodes:
        if n in nodes[k]['children']:
            is_child = True
            break

    if not is_child:
        parent = n
        break

print("parent:", parent)

def nodesum(n):
    if len(nodes[n]['children']) == 0:
        return sum(nodes[n]['metadata'])
    else:
        return sum([nodesum(nodes[n]['children'][x-1]) for x in nodes[n]['metadata'] if x > 0 and x <= len(nodes[n]['children'])])

print(nodesum(parent))
pass

