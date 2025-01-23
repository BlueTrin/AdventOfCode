from aoc_lube import fetch
import re

s = fetch(2020, 4)

print(s)

def read(s):
    raw_passports = s.split('\n\n')

    passports = []
    for raw in raw_passports:
        passports.append({ (fv:=entry.split(':'))[0]: fv[1] for entry in raw.split() })
    return passports


passports = read(s)
valid = 0
for p in passports:
    if p.keys() >= {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}:
        valid += 1

print(f"Part1: {valid}")
# byr (Birth Year) - four digits; at least 1920 and at most 2002.
# iyr (Issue Year) - four digits; at least 2010 and at most 2020.
# eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
# hgt (Height) - a number followed by either cm or in:
# If cm, the number must be at least 150 and at most 193.
# If in, the number must be at least 59 and at most 76.
# hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
# ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
# pid (Passport ID) - a nine-digit number, including leading zeroes.
# cid (Country ID) - ignored, missing or not.

def p2_check(passports):
    valid = 0
    for p in passports:
        if not p.keys() >= {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}:
            continue
        if not (1920 <= int(p['byr']) <= 2002):
            continue
        if not (2010 <= int(p['iyr']) <= 2020):
            continue
        if not (2020 <= int(p['eyr']) <= 2030):
            continue
        if not (m:=re.match(r'(\d+)(cm|in)', p['hgt'])):
            continue
        h, u = m.groups()
        if u == 'cm' and not (150 <= int(h) <= 193):
            continue
        elif u == 'in' and not (59 <= int(h) <= 76):
            continue

        if not re.match(r'#[0-9a-f]{6}$', p['hcl']):
            continue
        if p['ecl'] not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
            continue
        if not re.match(r'\d{9}$', p['pid']):
            continue
        valid += 1
    return valid

valid = p2_check(read('''eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007'''))
assert valid == 0

valid = p2_check(read('''pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719'''))
assert valid == 4

valid = p2_check(passports)
print(f"Part2: {valid}")
#161 too high
