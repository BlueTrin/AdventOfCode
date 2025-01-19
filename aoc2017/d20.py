from aoc_lube import fetch
import math
from utils.utils import Point3D
import itertools
from collections import defaultdict, Counter

s = fetch(2017, 20)

print(s)

def read_particles(s):
    particles = []
    for r in s.splitlines():
        ps, vs, as_ = r.split(", ")
        p = Point3D(*list(map(int, ps[3:-1].split(","))))
        v = Point3D(*list(map(int, vs[3:-1].split(","))))
        a = Point3D(*list(map(int, as_[3:-1].split(","))))

        particles.append((p, v, a))
    return particles

particles = read_particles(s)
min_acc = None
min_acc_idx = None
# Part1: get the particle with the smallest acceleration
for i in range(1, len(particles)):
    if min_acc is None or Point3D(0, 0, 0).manhattan(particles[i][2]) < min_acc:
        min_acc = Point3D(0, 0, 0).manhattan(particles[i][2])
        min_acc_idx = i

print(f"Part1: {min_acc_idx}")

def pos(p, t):
    return p[0] + p[1]*t + p[2]*(t**2)/2

def solve_collision(p1, p2):
    # solve collision between two particles
    # if they collide, return the time of collision
    # else return None
    # p1 = (p1, v1, a1)
    # p2 = (p2, v2, a2)
    p1, v1, a1 = p1
    p2, v2, a2 = p2

    a = a1 - a2
    b = v1 - v2
    c = p1 - p2
    if a.x == 0 and b.x == 0:
        if c.x == 0:
            # they are already colliding
            return 0
        else:
            return None
    elif a.x == 0:
        # solve for t
        # p1 + v1*t = p2 + v2*t
        # t = (p2 - p1) / (v1 - v2)
        t = (p2.x - p1.x) / (v1.x - v2.x)
        sols = {t}
    else:
        # solve for t
        # p1 + v1*t + 0.5*a1*t^2 = p2 + v2*t + 0.5*a2*t^2
        # (a1 - a2)t^2 + (v1 - v2)t + (p1 - p2) = 0
        # quadratic formula
        # t = (-b +- sqrt(b^2 - 4ac)) / 2a
        if b.x**2 - 4*a.x*c.x < 0:
            return None
        tp = (-b.x + math.sqrt(b.x**2 - 4*a.x*c.x)) / (2*a.x)
        tn = (-b.x - math.sqrt(b.x**2 - 4*a.x*c.x)) / (2*a.x)
        sols = {tp, tn}
    # keep only positive integer solutions
    sols = {int(x) for x in sols if x >=0 and x.is_integer()}

    # check if the solutions are valid for Y and Z
    sols = {t for t in sols if p1 + v1*t + a1*(t**2)/2 == p2 + v2*t+ a2*(t**2)/2}

    if not sols:
        return None
    else:
        return min(sols)

def update_particles(particles):
    '''
    Increase the X velocity by the X acceleration.
    Increase the Y velocity by the Y acceleration.
    Increase the Z velocity by the Z acceleration.
    Increase the X position by the X velocity.
    Increase the Y position by the Y velocity.
    Increase the Z position by the Z velocity.
    '''
    for i in range(len(particles)):
        if particles[i] is None:
            continue
        p, v, a = particles[i]
        v += a
        p += v
        particles[i] = (p, v, a)
    return particles

NON_COLLISION_THRESHOLD = 1000
non_collition_time = 0
while non_collition_time < NON_COLLISION_THRESHOLD:
    non_collition_time += 1
    update_particles(particles)
    collisions = Counter([p[0] for p in particles])
    for p, c in collisions.items():
        if c > 1:
            non_collition_time = 0
            for i in range(len(particles)):
                if particles[i] is None:
                    continue
                if particles[i][0] == p:
                    particles[i] = None

    particles = [p for p in particles if p is not None]
print(f"Part2: {len(particles)}")


particles_ex = read_particles('''p=<-6,0,0>, v=<3,0,0>, a=<0,0,0>
p=<-4,0,0>, v=<2,0,0>, a=<0,0,0>
p=<-2,0,0>, v=<1,0,0>, a=<0,0,0>''')
assert solve_collision(particles_ex[0], particles_ex[1]) == 2

# collisions = defaultdict(list)
# for i1, i2 in itertools.combinations(range(len(particles)), 2):
#     p1 = particles[i1]
#     p2 = particles[i2]
#     t = solve_collision(p1, p2)
#     if t is not None:
#         collisions[t].append((i1, i2))
#
# pass