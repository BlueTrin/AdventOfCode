i=0
while True:
    import hashlib
    m = hashlib.md5()
    text = f"iwrupvqb{i}"
    m.update(text.encode('UTF-8'))
    s=m.hexdigest()
    if s.startswith("000000"):
        print(s)
        print(i)
        break
    
    i+=1

m=hashlib.md5()
m.update("abcdef609043".encode('UTF-8'))
print(m.hexdigest())