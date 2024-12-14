p1_ex = '''WORDS:THE,OWE,MES,ROD,HER

AWAKEN THE POWER ADORNED WITH THE FLAMES BRIGHT IRE'''

import re

def part1(txt):
    words_ln, _, last_ln = txt.splitlines()
    _, wordstr = words_ln.split(":")
    word_lst = wordstr.split(",")
    total = 0
    for word in word_lst:
        total += len(re.findall(word, last_ln))
    return total

print(part1(p1_ex))

p1_inp = '''WORDS:LOR,LL,SI,OR,DO,IR,IS

LOREM IPSUM DOLOR SIT AMET, CONSECTETUR ADIPISCING ELIT, SED DO EIUSMOD TEMPOR INCIDIDUNT UT LABORE ET DOLORE MAGNA ALIQUA. UT ENIM AD MINIM VENIAM, QUIS NOSTRUD EXERCITATION ULLAMCO LABORIS NISI UT ALIQUIP EX EA COMMODO CONSEQUAT. DUIS AUTE IRURE DOLOR IN REPREHENDERIT IN VOLUPTATE VELIT ESSE CILLUM DOLORE EU FUGIAT NULLA PARIATUR. EXCEPTEUR SINT OCCAECAT CUPIDATAT NON PROIDENT, SUNT IN CULPA QUI OFFICIA DESERUNT MOLLIT ANIM ID EST LABORUM.'''
print(part1(p1_inp))

def return_occurences(longstr, substr):
    ret = []
    i = 0
    while (pos:=longstr.find(substr, i)) != -1:
        ret.append(pos)
        i = pos + 1
    return ret


p2_ex = '''WORDS:THE,OWE,MES,ROD,HER,QAQ

AWAKEN THE POWE ADORNED WITH THE FLAMES BRIGHT IRE
THE FLAME SHIELDED THE HEART OF THE KINGS
POWE PO WER P OWE R
THERE IS THE END
QAQAQ'''
def part2(txt):
    words_ln, _, *last_ln_lst = txt.splitlines()

    _, wordstr = words_ln.split(":")
    word_lst = wordstr.split(",")
    total = 0
    for last_ln in last_ln_lst:
        runes_pos = set()
        for word in word_lst:
            for pos in return_occurences(last_ln, word) + return_occurences(last_ln, word[::-1]):
                for x in range(len(word)):
                    runes_pos.add(x + pos)
        total += len(runes_pos)
    return total

print(part2(p2_ex))

p2_inp = open(r"q2_p2_inp.txt").read()
print(part2(p2_inp))

p3_inp = '''WORDS:THE,OWE,MES,ROD,RODEO

HELWORLT
ENIGWDXL
TRODEOAL'''
N = -1j
S = 1j
W = -1
E = 1

NW = N + W
NE = N + E
SW = S + W
SE = S + E
from adventofcode.utils import parse_complex

# def modulo_im(pos, bottom_right_pt):
#     return  pos.real % (bottom_right_pt.real + 1) + 1j * (pos.imag % (bottom_right_pt.imag + 1))

def modulo_im(pos, bottom_right_pt):
    return  pos.real % (bottom_right_pt.real ) + 1j * pos.imag

def part3(txt):
    words_ln, _, *last_ln_lst = txt.splitlines()
    _, wordstr = words_ln.split(":")
    word_lst = wordstr.split(",")

    coords_to_char, char_to_coordsset, max_coords = parse_complex('\n'.join(last_ln_lst))

    runes_set = set()
    for x in coords_to_char:
        for word in word_lst:
            if coords_to_char[x] == word[0]:
                for dir in [N, S, W, E]:
                    to_match = [(i * dir, w) for i, w in enumerate(word)]
                    if all( coords_to_char.get(modulo_im(x + m_pos, max_coords)) == m_let for m_pos, m_let in to_match):
                        runes_set |= set((modulo_im(x + m_pos, max_coords) for m_pos, _ in to_match))
    return len(runes_set)

print(part3(p3_inp))
p3_inp = open(r"q2_p3_inp.txt").read()
print(part3(p3_inp))