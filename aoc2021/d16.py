from aoc_lube import fetch
from collections import deque
from functools import reduce
from operator import mul, add, gt, lt, eq
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
s = fetch(2021, 16)
# print(s)

def p1_solve(s, debug=False):
    d = deque()
    for c in s:
        d.append(f"{int(c, 16):04b}")

    # what do you get if you add up the version numbers in all packets?
    p1 = 0
    while True:
        p = get_packet(d, debug)
        if p is None:
            break

        ver, typeid, nfo = p
        p1 += ver
    return p1

def get_packet(d, debug=False) -> (tuple, None):
    remaining = ''
    while d:
        while len(remaining) < 6 and d:
            remaining += d.popleft()

        if not d and not remaining:
            return None
        ver = int(remaining[:3], 2)
        typeid = int(remaining[3:6], 2)
        remaining = remaining[6:]
        logger.debug(f"ver: {ver}, typeid: {typeid}")
        if typeid == 4:
            # Packets with type ID 4 represent a literal value. Literal value packets encode a single binary number. To do
            # this, the binary number is padded with leading zeroes until its length is a multiple of four bits, and then it is
            # broken into groups of four bits. Each group is prefixed by a 1 bit except the last group, which is prefixed by a
            # 0 bit. These groups of five bits immediately follow the packet header.
            while True:
                while len(remaining) < 5:
                    remaining += d.popleft()
                val = ''
                if remaining[0] == '0':
                    val += remaining[1:5]
                    logger.debug(f"  val={int(val,2)}")
                    remaining = remaining[5:]
                    d.appendleft(remaining)

                    return ver, typeid, int(val, 2), None
                else:
                    val += remaining[1:5]
                    remaining = remaining[5:]
        else:
            while len(remaining) < 1:
                remaining += d.popleft()
            lengthid = int(remaining[:1], 2)

            logger.debug(f"  lengthid={lengthid}")

            remaining = remaining[1:]
            if lengthid == 0:
                # If the length type ID is 0, then the next 15 bits are a number that represents the total length in bits of
                # the sub-packets contained by this packet.
                while len(remaining) < 15:
                    remaining += d.popleft()
                len_subpackets = int(remaining[:15], 2)

                logger.debug(f"  total_len={len_subpackets}")

                remaining = remaining[15:]
                d.appendleft(remaining)
                return ver, typeid, lengthid, len_subpackets

            elif lengthid == 1:
                # If the length type ID is 1, then the next 11 bits are a number that represents the number of sub-packets
                # immediately contained by this packet.
                while len(remaining) < 11:
                    remaining += d.popleft()
                sub_sz = int(remaining[:11], 2)

                logger.debug(f"  num subpackets={sub_sz}")

                remaining = remaining[11:]

                d.appendleft(remaining)
                assert sub_sz > 0

                return ver, typeid, lengthid, sub_sz

    return None

# t = p1_solve('''EE00D40C823060''', debug=False)
#
# p1 = p1_solve(s)
# print(f"Part1: {p1}")


def p2_solve(s, debug=False):
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    d = deque()
    for c in s:
        d.append(f"{int(c, 16):04b}")
    if debug:
        logger.debug(''.join([c for c in d]))
    return p2_impl(d)

def p2_impl(d):
    # what do you get if you add up the version numbers in all packets?
    p2 = 0
    while True:
        p = get_packet(d)
        if p is None:
            break

        ver, typeid, nfo, subpackets_nfo = p
        if typeid == 4:
            logger.debug(f"LITERAL = {nfo}")
            p2 += nfo
        else:
            p2 += fn(typeid, nfo, subpackets_nfo, d)
        return p2

def fn(typeid, lengthid, subpackets_nfo, d, debug=False):
    logger.debug(f"fn({typeid}, {lengthid}, {subpackets_nfo})")
    if lengthid == 0:
        # Packets with length type ID 0 contain a number that represents the total length in bits of the sub-packets
        # contained by this packet. The sub-packets are packed into the remaining bits of the packet, and the packet
        # is padded with zeroes if necessary to make its length a multiple of eight bits.
        subpacket_s = ''
        while len(subpacket_s) < subpackets_nfo:
            subpacket_s += d.popleft()
        pd = deque()
        pd.append(subpacket_s[:subpackets_nfo])
        d.appendleft(subpacket_s[subpackets_nfo:])

        p = []
        while pd:
            v = p2_impl(pd)
            if v is not None:
                p.append(v)
    elif lengthid == 1:
        # Packets with length type ID 1 contain a number that represents the number of sub-packets immediately contained
        # by this packet. The sub-packets are packed
        p = [p2_impl(d) for _ in range(subpackets_nfo)]
    else:
        raise RuntimeError(f"Unknown lengthid: {lengthid}")

    assert len(p) >= 1
    # Packets with type ID 0 are sum packets - their value is the sum of the values of their sub-packets.
    # If they only have a single sub-packet, their value is the value of the sub-packet.
    if typeid == 0:
        res = sum(p)
        logger.debug(f"SUM = {res} <- {p}")

    # Packets with type ID 1 are product packets - their value is the result of multiplying together the values of
    # their sub-packets. If they only have a single sub-packet, their value is the value of the sub-packet.
    elif typeid == 1:
        res = reduce(mul, p, 1)
        logger.debug(f"MUL = {res} <- {p}")

    # Packets with type ID 2 are minimum packets - their value is the minimum of the values of their sub-packets.
    elif typeid == 2:
        res = min(p)
        logger.debug(f"MIN = {res} <- {p}")

    # Packets with type ID 3 are maximum packets - their value is the maximum of the values of their sub-packets.
    elif typeid == 3:
        res = max(p)
        logger.debug(f"MAX = {res} <- {p}")

    # Packets with type ID 5 are greater than packets - their value is 1 if the value of the first sub-packet is
    # greater than the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly
    # two sub-packets.
    elif typeid == 5:
        assert len(p) == 2
        res = int(p[0] > p[1])
        logger.debug(f"> = {res} <- {p}")

    # Packets with type ID 6 are less than packets - their value is 1 if the value of the first sub-packet is less than
    # the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    elif typeid == 6:
        assert len(p) == 2
        res = int(p[0] < p[1])
        logger.debug(f"< = {res} <- {p}")

    # Packets with type ID 7 are equal to packets - their value is 1 if the value of the first sub-packet is equal to
    # the value of the second sub-packet; otherwise, their value is 0. These packets always have exactly two sub-packets.
    elif typeid == 7:
        assert len(p) == 2
        res = int(p[0] == p[1])
        logger.debug(f"== = {res} <- {p}")

    else:
        raise RuntimeError(f"Unknown typeid: {typeid}")

    return res

# C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
# assert p2_solve('''C200B40A82''', debug=True) == 3

# 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
# assert p2_solve('''04005AC33890''', debug=True) == 54

# 880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
# assert p2_solve('''880086C3E88112''', debug=True) == 7

# CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
# assert p2_solve('''CE00C43D881120''', debug=True) == 9

# D8005AC2A8F0 produces 1, because 5 is less than 15.
# assert p2_solve('''D8005AC2A8F0''', debug=True) == 1

# F600BC2D8F produces 0, because 5 is not greater than 15.
# assert p2_solve('''F600BC2D8F''', debug=True) == 0

# 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
# assert p2_solve('''9C005AC2F8F0''', debug=True) == 0

# 9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.
# assert p2_solve('''9C0141080250320F1802104A08''', debug=True) == 1

p2 = p2_solve(s, debug=True)
print(f"Part2: {p2}")

# 78328 too low