n = 9
m = 27

for i in range(n+1):
    pattern = "!*!" * (i)
    p1 = pattern.ljust(m , ":")
    p2 = pattern.rjust(m , ":")
    print(p1 + p2)