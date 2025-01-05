from aoc_lube import fetch
from utils2018.utils import Point3D as Point
import math
import numpy as np

s = fetch(2022, 22)

cube_s, path_s = s.split('\n\n')

y_len = len([r for r in cube_s.splitlines() if r])
x_len = len(cube_s.splitlines()[0])

side_l = min(x_len//3, y_len//3)
print("side_l", side_l)


def rot_x(pt, angle):
    from utils2018.utils import rotation_x_3d
    shift = Point(0, side_l/2 + 1, side_l/2 + 1)
    shifted_pt = rotation_x_3d(pt-shift, angle) + shift
    return Point(*[round(c) for c in shifted_pt])


def rot_y(pt, angle):
    from utils2018.utils import rotation_y_3d
    shift = Point(0, side_l/2 + 1, 0)
    shifted_pt = rotation_y_3d(pt-shift, angle) + shift
    return Point(*[round(c) for c in shifted_pt])


def rot_z(pt, angle):
    from utils2018.utils import rotation_z_3d
    shift = Point(0, 0, side_l/2 + 1)
    shifted_pt = rotation_z_3d(pt-shift, angle) + shift
    return Point(*[round(c) for c in shifted_pt])


start_coords = Point(None, None, None)
for x in range(x_len):
    if cube_s.splitlines()[0][x] != ' ':
        start_coords = Point(x, 0, 0)
        break



def read_face(curr_face, cube3d_pt, cubex_dir, cubey_dir):
    """
    Reads a face of the cube and returns a dictionary of the cube
    @param curr_face: top left corner of the 2d cube
    @param cube3d_pt: the 3d point of the cube
    @param cubex_dir: the direction of the cube in the x axis
    @param cubey_dir: the direction of the cube in the y axis
    """
    cube2d = cube_s.splitlines()
    cube = {}
    for y in range(curr_face.y, curr_face.y+side_l):
        for x in range(curr_face.x, curr_face.x+side_l):
            tgt_pt = cube3d_pt + cubex_dir * (x - curr_face.x) + cubey_dir * (y - curr_face.y)
            cube[tgt_pt] = cube2d[y][x]


    if cube2d[curr_face.y][curr_face.x+side_l] != ' ':
        add_pts = read_face(cube3d_pt + cubex_dir * side_l, cube3d_pt, rot_x(cubex_dir, 90), rot_x(cubey_dir, 90))
        raise RuntimeError("Invalid input")
    if cube2d[curr_face.y+side_l][curr_face.x] != ' ':
        raise RuntimeError("Invalid input")
    return cube

curr_face = start_coords

cube = read_face(
    curr_face,
    Point(1, 51, 52),
    Point(1, 0, 0),
    Point(0, -1, 0),
)

pass