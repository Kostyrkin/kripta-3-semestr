import random

def EA(x, y):
    a2, a1, b2, b1 = 1, 0, 0, 1

    while y:
        q = x // y
        r = x - q * y
        a = a2 - q * a1
        b = b2 - q * b1
        x = y
        y = r
        a2 = a1
        a1 = a
        b2 = b1
        b1 = b
    b = b2
    return b

def gen_key():
    #n = int(input("Введите колличество пользователей:"))
    F = 65537
    n = 3
    r = []
    fl = 0

    while fl < n:
        r_p = random.randint(1, F)
        if not r_p in r:
            r.append(r_p)
            fl += 1

    t = random.randint(1, n-1)
    a = []
    for i in range(t+1):
        a.append(random.randint(1, F))

    S = a[0]
    s = []
    for i in range(n):
        s_i = a[0]
        for j in range(1, t+1):
            s_i += a[j]*pow(r[i], j)
        s.append(s_i)
    #print("a:", a)
    #print("r:", r)
    #print("s:", s)
    #проверка
    S_p = 0
    for i in range(t+1):
        mp = 1
        for j in range(t+1):
            if j != i:
                c_n_obr = EA(F, pow(r[j] - r[i], 1, F))
                mp = mp*(r[j]*c_n_obr)
        S_p += s[i]*mp
    #print(S, S_p)
    #print(S, pow(round(S_p), 1, F))
    if S == round(S_p) or S == pow(round(S_p), 1, F):
        return True

ch = 0
for i in range(10000):
    a = gen_key()
    if a:
        ch += 1
print(ch)
