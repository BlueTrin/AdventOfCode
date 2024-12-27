import re

rng = {chr(i): i-ord('a') for i in range(ord('a'), ord('z')+1)}
curr = "hepxcrrq"
nb = sum(26**i * rng[c] for i, c in enumerate(reversed(curr)))


def nb2s(d):
    s = ""
    while d:
        s = chr(ord('a') + d%26) + s
        d = d//26
    return s


def has_seq(s):
    return any(ord(a) == ord(b)-1 == ord(c)-2 for a, b, c in
               zip(s, s[1:], s[2:]))


def valid_c(s):
    return "i" not in s and "o" not in s and "l" not in s


def has_double(s):
    return len(re.findall(r"([a-z])\1", s)) >= 2


assert has_seq("fhyhbcdug")
assert not valid_c("dfgdflg")
assert has_double("aagbb")

res=[]
while True:
    nb += 1
    s = nb2s(nb)
    if has_seq(s) and valid_c(s) and has_double(s):
        print(s)
        res.append(s)
        if len(res) >= 2:
            raise RuntimeError("toto")
    # print(s)


print(s)