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
    m = x
    b = b2
    return m, b
    # d=a a=u b=v au + bv = gcd(a, b).


# Prime number function(нахождение простого числа)
def PMF(k, t):
    import random

    while True:
        p = ""
        for i in range(k - 2):
            p = str(random.randint(0, 1)) + p
        p = "1" + p + '1'
        p = int(p, 2)
        flag = 1
        if p == 2:
            return True
        if not p & 1:
            return False

        def check(a, s, d, p):
            x = pow(a, d, p)
            if x == 1:
                return True
            for i in range(s - 1):
                if x == p - 1:
                    return True
                x = pow(x, 2, p)
            return x == p - 1

        s = 0
        d = p - 1
        while d % 2 == 0:
            d >>= 1
            s += 1
        for i in range(t):
            a = random.randint(2, p - 2)
            if not check(a, s, d, p):
                flag = 0
        if flag == 1:
            return p

# Cipher RSA(Шифр RSA)
def C_RSA():
    import random
    k = 1024

    p = PMF(k, 100)
    q = PMF(k, 100)
    n = p * q
    x = (p - 1) * (q - 1)
    while True:
        e = random.randint(2, 50)
        m, d = EA(x, e)
        if m == 1:
            break
    SubjectPublicKeyInfo = {"publicExponent": e, "N": n}
    p_k = {"SubjectPublicKeyInfo": SubjectPublicKeyInfo, "PKCS10CertRequest": "NULL", "Certificate": "NULL",
           "PKCS7CertChain-PKCS": "NULL"}

    c_k = {"privateExponent": d, "prime1": p, "prime2": q, "exponent1": pow(d, 1, (p - 1)),
           "exponent2": pow(d, 1, (q - 1)), "coefficient": pow(q, -1, p)}

    return c_k