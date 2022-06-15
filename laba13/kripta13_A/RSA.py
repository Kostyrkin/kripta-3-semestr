import random
import json

class RSA:
    def __init__(self):
        pass

    # Euclid's algorithm(алгорим Евклида)
    def EA(self, x, y):
        a2, a1, b2, b1 = 1, 0, 0, 1

        while y:
            q = x // y
            r = x - q*y
            a = a2 - q*a1
            b = b2 - q*b1
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
    def PMF(self, k, t):
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

    def mod_text_in_bit(self, text: str) -> str:
        bit_text = ''
        encode_text = text.encode('utf-8')
        for i in range(len(encode_text)):
            bit_text = bit_text + '0' * (8 - len(format(encode_text[i], 'b'))) + format(encode_text[i], 'b')
        return bit_text

    def block(self, n):
        n = len(bin(int(n))[2:])
        i = 0
        while True:
            if pow(2, i) < n:
                i += 1
            elif pow(2, i-1) < 2048:
                return pow(2, i-1) - 16
            else:
                return 2032

    # Cipher RSA(Шифр RSA)
    def C_RSA(self):
        p = self.PMF(100, 100)
        q = self.PMF(100, 100)
        n = p * q
        x = (p-1)*(q-1)
        while True:
            e = random.randint(2, 50)
            m, d = self.EA(x, e)
            if m == 1:
                break
        SubjectPublicKeyInfo = {"publicExponent": e, "N": n}
        p_k = {"SubjectPublicKeyInfo": SubjectPublicKeyInfo, "PKCS10CertRequest":"NULL", "Certificate":"NULL", "PKCS7CertChain-PKCS":"NULL"}
        with open("ok_user.json", "w", encoding="utf-8") as file:
            json.dump(p_k, file)

        c_k = {"privateExponent": d, "prime1": p, "prime2": q, "exponent1": pow(d, 1, (p-1)), "exponent2": pow(d, 1, (q-1)), "coefficient": pow(q, -1, p)}
        with open("zk_user.json", "w", encoding="utf-8") as file:
            json.dump(c_k, file)

        return c_k

    def coding(self, Met, Sv, M):
        with open("ok_user.json", "r", encoding="utf-8") as file:
            p_k = json.load(file)
        e = p_k["SubjectPublicKeyInfo"]["publicExponent"]
        n = p_k["SubjectPublicKeyInfo"]["N"]
        A = ["512", "256"]
        B = ["GOST", "SHA"]
        M_m = []
        enc_M = ""
        block = self.block(n)
        for i in range(0, len(M), block):
            if len(M) - i < block:
                a = int(((block + 8) - (len(M) - i)) / 8)
                M_m.append(M[i:] + str(bin(a))[2:].zfill(8) * a)
            else:
                M_m.append(M[i:i + block] + "00000001")
        for i in M_m:
            a = hex((pow(int(i, 2), e, n)))[2:]
            a = "0"*(len(hex(n)[2:])-len(a)) + a
            enc_M += a
        c = B[int(Met) - 1] + A[int(Sv) - 1]
        c_m = {"Version": 0, "EncryptedContentInfo": {"ContentType": "text", "ContentEncryptionAlgorithmIdentifier": "rsaEncryption", "encryptedContent": enc_M, "OPTIONAL":{"DigestAlgorithmIdentifiers": c}}}
        return c_m

    def decoding(self):
        with open(input("Введите название файла c закрытым ключем:") + ".json", "r", encoding="utf-8") as file:
            c_k = json.load(file)
        with open(input("Введите название файла c зашифрованным текстом:") + ".json", "r", encoding="utf-8") as file:
            c_m = json.load(file)
        enc_M = c_m["EncryptedContentInfo"]["encryptedContent"]
        d = c_k["privateExponent"]
        n = c_k["prime1"] * c_k["prime2"]
        M_m = []
        M = ""
        block = self.block(n)

        for i in range(0, len(enc_M), len(hex(n)[2:])):
            M_m.append(enc_M[i:i + len(hex(n)[2:])])
        for i in M_m:
            a = bin(pow(int(i, 16), d, n))[2:]
            if len(a) < block + 8:
                a = "0"*(block + 8 - len(a)) + a
            M += a[:-(int(a[-8:], 2) * 8)]
        return M