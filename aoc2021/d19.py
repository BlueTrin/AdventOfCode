from aoc_lube import fetch
from utils.utils import rotation_x_3d, rotation_y_3d, rotation_z_3d, Point3D as Point
from collections import defaultdict
import logging
import itertools


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

s = fetch(2021, 19)

ROTATIONS = [
    c + (z,) for c in [
        (0, 0),
        (0, 90),
        (0, 180),
        (0, 270),
        (90, 0),
        (270, 0),
    ] for z in [0, 90, 180, 270]
]
# print(s)


def apply_rot(pt, x, y, z, inv=False):
    if inv:
        return rotation_x_3d(rotation_y_3d(rotation_z_3d(pt, z), y), x)
    else:
        return rotation_z_3d(rotation_y_3d(rotation_x_3d(pt, x), y), z)


def display_scanner_points_as_0(rot_from_0, pos_from_0, scan_pts):
    return {apply_rot(pt, *rot_from_0) + pos_from_0 for pt in scan_pts}


def solve(s: str):
    scan_pts = {}

    groups_s = s.split('\n\n')
    for group_s in groups_s:
        scan_s, *pos_s_lst = group_s.split('\n')
        scan_id = scan_s.replace("-", "").replace("scanner", '').strip()
        scan_id = int(scan_id)

        scan_pts[scan_id] = set()
        for pos_s in pos_s_lst:
            x, y, z = map(int, pos_s.split(','))
            pt = Point(x, y, z)
            scan_pts[scan_id].add(pt)

    import itertools
    from collections import Counter

    # make all rotations
    scans_rotated = {}
    for scan_id, scan_pt in scan_pts.items():
        for r in ROTATIONS:
            scans_rotated[(scan_id, r)] = {apply_rot(pt, *r) for pt in scan_pt}


    # for every combination make the translation vectors
    all_matches = {}

    positions = {
    0: ((0,0,0), Point(0, 0, 0)),
    }

    pts_from_scan0 = set()
    pts_from_scan0.update(scan_pts[0])
    scanners_from_t0 = {}
    ran_rotations = set()
    while len(positions) < len(scan_pts):
        for scan1_id, scan1_pts in scan_pts.items():
            logger.info(scan1_id)
            matches = []
            if scan1_id not in positions or scan1_id in ran_rotations:
                continue

            scan1_pts = {apply_rot(pt, *positions[scan1_id][0]) for pt in scan1_pts}
            for (scan2_id, r2), scan2_pts in scans_rotated.items():
                if scan1_id == scan2_id:
                    continue
                if scan2_id in positions:
                    continue

                c = Counter()
                for pt1, pt2 in itertools.product(scan1_pts, scan2_pts):
                    c[pt1 - pt2] += 1

                if c.most_common(1)[0][1] >= 12:
                    assert c.most_common(1)[0][1] == 12
                    matches.append((scan2_id, r2, c.most_common(1)[0]))

                    tot_r = r2
                    # tot_r = tuple(x % 360 for x in Point(*r2) + Point(*positions[scan1_id][0]))
                    #
                    # vec_scan1_to_scan2_in_0 = apply_rot(
                    #     c.most_common(1)[0][0],
                    #     *tuple(Point(*positions[scan1_id][0])),
                    # )

                    pos_from_0 = c.most_common(1)[0][0] + positions[scan1_id][1]
                    scanners_from_t0[scan2_id] = pos_from_0

                    # scanner 1 must be at 68,-1246,-43
                    # scanner 2 must be at 1105,-1205,1229
                    # scanner 3 must be at -92,-2380,-20
                    # scanner 4 is at -20,-1133,1061
                    logger.info(f"scan2_id: {scan2_id}, roration from scan0 : {tot_r}, pos_from_0: {pos_from_0}")
                    scan2_pts_as_0 = display_scanner_points_as_0(tot_r, pos_from_0, scan_pts[scan2_id])
                    assert len(set.intersection(pts_from_scan0, scan2_pts_as_0)) >= 12
                    pts_from_scan0.update(scan2_pts_as_0)

                    positions[scan2_id] = tot_r, pos_from_0
            all_matches[scan1_id] = matches
            ran_rotations.add(scan1_id)

    return pts_from_scan0, scanners_from_t0

# 467 too high
# 335 too low

ex = '''--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14'''

pts, _ = solve(ex)
assert len(pts) == 79

pts, scanners_from_t0 = solve(s)
print(f"Part1: {len(pts)}")

p2 = 0
for scan1, scan2 in itertools.combinations(scanners_from_t0.values(), 2):
    p2 = max(p2, scan1.manhattan(scan2))

print(f"Part2: {p2}")