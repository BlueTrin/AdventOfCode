from utils import primes

a=b=c=d=e=f=g=h=0
a=1
#b = 109900
c = 126900

prime_lst = primes(126901)
# 8 to 10
for b in range(109900, c+1, 17):
    if b not in prime_lst: # 24
        h += 1

print(h)