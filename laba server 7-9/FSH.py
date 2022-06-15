import random
import json

import SHA
import Stribog


class FSH:
    def __init__(self):
        pass

    # Euclid's algorithm(алгорим Евклида)
    def EA(self, x, y):
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

    # Cipher RSA(Шифр RSA)
    def C_FSH(self, Sv):
        p = self.PMF(100, 100)
        q = self.PMF(100, 100)
        n = p * q
        a = []
        b = []
        if Sv == "512":
            m = 512
        else:
            m = 256
        k = 0
        while k < m:
            a_r = random.randint(0, n)
            if not a_r in a:
                a.append(a_r)
                k += 1
        for i in range(m):
            fix, a_1 = self.EA(n, a[i])
            b.append(pow(a_1, 2, n))


        SubjectPublicKeyInfo = {"publicExponent": b, "N": n}
        p_k = {"SubjectPublicKeyInfo": SubjectPublicKeyInfo, "PKCS10CertRequest":"NULL", "Certificate":"NULL", "PKCS7CertChain-PKCS":"NULL"}
        with open("ok_FSH.json", "w", encoding="utf-8") as file:
            json.dump(p_k, file, indent=4)

        c_k = {"privateExponent": a, "prime1": p, "prime2": q}
        with open("zk_FSH.json", "w", encoding="utf-8") as file:
            json.dump(c_k, file, indent=4)

    def coding(self, Mes, hesh_f, timestamp, type_hesh):
        self.C_FSH(type_hesh[-3:])
        with open("zk_FSH.json", "r", encoding="utf-8") as file:
            c_k = json.load(file)
        a = c_k["privateExponent"]
        n = c_k["prime1"] * c_k["prime2"]
        hesh_f = hex(int(str(int(hesh_f["s"], 2)) + hesh_f["t"]))[2:]

        M = self.mod_text_in_bit(Mes)

        H_i = ""
        for i in range(len(hesh_f)):
            H_i = H_i + bin(int(hesh_f[i], 16))[2:].zfill(4)

        M = M + H_i + timestamp

        # 1 этап
        r = random.randint(1, (n-1))
        # 2 этап
        u = pow(r, 2, n)
        # 3 этап
        if type_hesh == "GOST512":
            s = Stribog.heshf().hesh_function((M + str(bin(u))[2:]), "1")
        elif type_hesh == "GOST256":
            s = Stribog.heshf().hesh_function((M + str(bin(u))[2:]), "2")
        elif type_hesh == "SHA512":
            s = SHA.SHA().SHA_function((M + str(bin(u))[2:]), "1")
        elif type_hesh == "SHA256":
            s = SHA.SHA().SHA_function((M + str(bin(u))[2:]), "2")
        # 4 этап
        a_i = 1
        for i in range(int(type_hesh[-3:])):
            a_i = a_i * pow(a[i], int(s[i]))
        t = pow(r * a_i, 1, n)
        S = {"s": s, "t": str(t)}
        return M, S



    def Provreka_h(self, c_m):
        type_hesh = c_m['DigestAlgorithmIdentifiers']
        M = c_m['EncapsulatedContentInfo']['OCTET STRING OPTIONAL']
        s = c_m['SignerInfos']['SignatureValue']['s']
        t = c_m['SignerInfos']['SignatureValue']['t']
        b = c_m["CertificateSet OPTIONAL"]["SubjectPublicKeyInfo"]["publicExponent"]
        n = c_m["CertificateSet OPTIONAL"]["SubjectPublicKeyInfo"]["N"]

        M = self.mod_text_in_bit(M)

        b_i = 1
        for i in range(int(type_hesh[-3:])):
            b_i = b_i * pow(b[i], int(s[i]))
        w = pow(pow(int(t), 2) * b_i, 1, n)

        if type_hesh == "GOST512":
            s_p = Stribog.heshf().hesh_function((M + str(bin(w))[2:]), "1")
        elif type_hesh == "GOST256":
            s_p = Stribog.heshf().hesh_function((M + str(bin(w))[2:]), "2")
        elif type_hesh == "SHA512":
            s_p = SHA.SHA().SHA_function((M + str(bin(w))[2:]), "1")
        elif type_hesh == "SHA256":
            s_p = SHA.SHA().SHA_function((M + str(bin(w))[2:]), "2")

        if s == s_p:
            print("Signature is correct")
            return False
        else:
            print("Signature is incorrect")
            return True