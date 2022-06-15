import random
import json
import time

import requests
import threading

import SHA
import Stribog


class GP:
    def __init__(self):
        self.kol_pol = 2

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

            mas = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
            if p in mas:
                return p

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

    def Mr(self, p, t):
        mas = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        if p in mas:
            return True
        flag = 1

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
            return True
        else:
            return False

    def mod_text_in_bit(self, text: str) -> str:
        bit_text = ''
        encode_text = text.encode('utf-8')
        for i in range(len(encode_text)):
            bit_text = bit_text + '0' * (8 - len(format(encode_text[i], 'b'))) + format(encode_text[i], 'b')
        return bit_text

    def save_object(self, name, obj):
        with open("object.json", "r", encoding='utf-8') as file:
            mas = json.load(file)
        mas[name] = obj
        with open("object.json", "w", encoding='utf-8') as file:
            json.dump(mas, file, indent=4)

    # Cipher RSA(Шифр RSA)
    def C_GP(self):
        n = 1024
        p = self.PMF(n, 100)

        numb = p - 1
        q = 1
        div = 2
        flag = False
        while numb > 1:
            while numb % div == 0:
                numb = numb // div
                if div > 547:
                    q = div
                    flag = True
                if numb > 1 and self.Mr(numb, 100):
                    q = numb
                    flag = True
            if flag:
                break
            div += 1

        while True:
            af = self.PMF(random.randint(3, n), 100)
            if pow(int(af), 2, int(p)) != 1 and pow(int(af), int((p - 1) / 2), int(p)) != 1 and int(af) < int(p):
                break
        k = int((p - 1) / q)
        af = pow(af, k, p)
        self.save_object("p", p)
        self.save_object("q", q)
        self.save_object("alfa", af)

        url = 'http://localhost:8880'
        req = requests.get(url)
        p_k = json.loads(req.text)
        d = p_k["privateExponent"]
        n = p_k["prime1"] * p_k["prime2"]
        self.save_object("d", d)
        self.save_object("n", n)

        z = random.randint(1, p - 1)
        L = pow(af, z, p)
        self.save_object("z", z)
        self.save_object("L", L)

        mes = {"p":p, "q":q, "alfa":af}
        for i in range(self.kol_pol):
            url = 'http://localhost:8' + str(i).zfill(4 - len(str(i)))
            requests.post(url, params="Key",json=mes)

    def coding(self, Met, Sv):
        with open("object.json", "r", encoding="utf-8") as file:
            info = json.load(file)

        d = info["d"]
        p = info["p"]
        q = info["q"]
        n = info["n"]
        af = info["alfa"]
        z = info["z"]
        P = info["P"]
        L = info["L"]

        Mes = input("Введите сообщение:")
        M = self.mod_text_in_bit(Mes)

        # 1 этап
        if Met == "1":
            H = int(Stribog.heshf().hesh_function(M, Sv), 2)
        else:
            H = int(SHA.SHA().SHA_function(M, Sv), 2)

        ld = []
        for i in range(self.kol_pol):
            ld.append(pow((H + info["P"][i]), d, n))

        U = 1
        for i in range(self.kol_pol):
            U = U * pow(info["P"][i], ld[i], p)

        # 2 этап
        R_i = []
        for i in range(self.kol_pol):
            url = 'http://localhost:8' + str(i).zfill(4 - len(str(i)))
            req = requests.post(url, data=str(ld[i]), params="Stage1")
            R_i.append(int(req.text))

        # 3 этап
        T = random.randint(1, q)
        R = pow(af, T, p)
        for i in range(self.kol_pol):
            R = pow(R * R_i[i], 1, p)

        if Met == "1":
            E = int(Stribog.heshf().hesh_function((M+bin(R)[2:]+bin(U)[2:]), Sv), 2)
        else:
            E = int(SHA.SHA().SHA_function((M+bin(R)[2:]+bin(U)[2:]), Sv), 2)

        # 4 этап
        S_i = []
        for i in range(self.kol_pol):
            url = 'http://localhost:8' + str(i).zfill(4 - len(str(i)))
            req = requests.post(url, data=str(E), params="Stage2")
            S_i.append(int(req.text))
        # 5 этап
        for i in range(self.kol_pol):
            while True:
                m, P_ob = self.EA(p, P[i])
                if m == 1:
                    break
            ch_1 = pow(P_ob, ld[i]*E, p)
            ch_2 = pow(af, S_i[i], p)
            R_p = pow(ch_1*ch_2, 1, p)
            if R_i[i] == R_p:
                print("True")
            else:
                print(R_i[i], R_p)
                return print("Message not signed by group")
        S = pow((T + z*E), 1, q)
        S_q = 0
        for i in range(self.kol_pol):
            S_q = pow((S_q + S_i[i]), 1, q)
        S = pow((S + S_q), 1, q)
        sign = {"U":U, "E":E ,"S":S}

        A = ["512", "256"]
        B = ["GOST", "SHA"]
        c = B[int(Met) - 1] + A[int(Sv) - 1]

        c_m = {"CMSVersion": 1, "DigestAlgorithmIdentifiers": c,
               "EncapsulatedContentInfo": {"ContentType": "text", "OCTET STRING OPTIONAL": M},
               "CertificateSet OPTIONAL": {"L":L, "alfa":af, "p":p}, "RevocationInfoChoises OPTIONAL": "NULL",
               "SignerInfos": {"CMSVersion": 1, "SignerIdentifier": "Kostyrkin Nikita", "DigestAlgorithmIdentifier": c,
                               "SignedAttributes OPTIONAL": "NULL", "SignatureAlgorithmIdentifier": "RSAdsi",
                               "SignatureValue": sign, "UnsignedAttributes OPTIONAL": {"OBJECT IDENTIFIER": "NULL",
                                                                                        "SET OF AttributeValue": "NULL"}}}
        with open("Group_Signature.json", "w", encoding="utf-8") as file:
            json.dump(c_m, file, indent=4)
        self.Provreka(c_m)

    def Provreka(self, c_m):
        type_hesh = c_m["DigestAlgorithmIdentifiers"]
        M = c_m["EncapsulatedContentInfo"]["OCTET STRING OPTIONAL"]
        U = c_m["SignerInfos"]["SignatureValue"]["U"]
        E = c_m["SignerInfos"]["SignatureValue"]["E"]
        S = c_m["SignerInfos"]["SignatureValue"]["S"]
        L = c_m["CertificateSet OPTIONAL"]["L"]
        af = c_m["CertificateSet OPTIONAL"]["alfa"]
        p = c_m["CertificateSet OPTIONAL"]["p"]

        # 1 этап
        if type_hesh == "GOST512":
            H = Stribog.heshf().hesh_function(M, "1")
        elif type_hesh == "GOST256":
            H = Stribog.heshf().hesh_function(M, "2")
        elif type_hesh == "SHA512":
            H = SHA.SHA().SHA_function(M, "1")
        elif type_hesh == "SHA256":
            H = SHA.SHA().SHA_function(M, "2")

        # 2 этап
        while True:
            m, UL_ob = self.EA(p, (U*L))
            if m == 1:
                break
        ch_1 = pow(UL_ob, E, p)
        ch_2 = pow(af, S, p)
        R = pow(ch_1 * ch_2, 1, p)

        # 3 этап
        if type_hesh == "GOST512":
            E_p = int(Stribog.heshf().hesh_function((M+bin(R)[2:]+bin(U)[2:]), "1"), 2)
        elif type_hesh == "GOST256":
            E_p = int(Stribog.heshf().hesh_function((M+bin(R)[2:]+bin(U)[2:]), "2"), 2)
        elif type_hesh == "SHA512":
            E_p = int(SHA.SHA().SHA_function((M+bin(R)[2:]+bin(U)[2:]), "1"), 2)
        elif type_hesh == "SHA256":
            E_p = int(SHA.SHA().SHA_function((M+bin(R)[2:]+bin(U)[2:]), "2"), 2)

        if E == E_p:
            print("Group signature is correct")
        else:
            print("Group signature is not correct")

    def ran(self):
        flag1 = input("Метод хеширования:\n1)Стрибог\n2)SHA\n")
        flag2 = input("Свертка:\n1)512 бит\n2)256 бит\n")
        P = []
        for i in range(self.kol_pol):
            url = 'http://localhost:8' + str(i).zfill(4 - len(str(i)))
            req = requests.get(url)
            P.append(int(req.text))
        self.save_object("P", P)
        self.coding(flag1, flag2)


if __name__ == '__main__':
    obj = GP()
    obj.C_GP()
    obj.ran()
