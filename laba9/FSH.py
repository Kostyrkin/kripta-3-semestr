import random
import json
import requests

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
        if Sv == "1":
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

    def coding(self, Met, Sv):
        self.C_FSH(Sv)
        with open("ok_FSH.json", "r", encoding="utf-8") as file:
            p_k = json.load(file)
        with open("zk_FSH.json", "r", encoding="utf-8") as file:
            c_k = json.load(file)
        a = c_k["privateExponent"]
        n = c_k["prime1"] * c_k["prime2"]
        b = p_k["SubjectPublicKeyInfo"]["publicExponent"]

        A = ["512", "256"]
        B = ["GOST", "SHA"]

        Mes = input("Введите сообщение:")
        M = self.mod_text_in_bit(Mes)
        # 1 этап
        r = random.randint(1,(n-1))
        # 2 этап
        u = pow(r, 2, n)
        # 3 этап
        if Met == "1":
            s = Stribog.heshf().hesh_function((M + str(bin(u))[2:]), Sv)
        else:
            s = SHA.SHA().SHA_function((M + str(bin(u))[2:]), Sv)
        # 4 этап
        a_i = 1
        for i in range(int(A[int(Sv) - 1])):
            a_i = a_i * pow(a[i], int(s[i]))
        t = pow(r * a_i, 1, n)
        S = {"s": s, "t": str(t)}

        c = B[int(Met) - 1] + A[int(Sv) - 1]
        name = input("Введите название файла для записи зашифровонного текста:")
        c_m = {"CMSVersion": 1, "DigestAlgorithmIdentifiers": c, "EncapsulatedContentInfo": {"ContentType": "text", "OCTET STRING OPTIONAL": Mes}, "CertificateSet OPTIONAL": p_k, "RevocationInfoChoises OPTIONAL":"NULL", "SignerInfos":{"CMSVersion":1, "SignerIdentifier":"Kostyrkin Nikita", "DigestAlgorithmIdentifier": c, "SignedAttributes OPTIONAL": "NULL", "SignatureAlgorithmIdentifier": "FSAdsi", "SignatureValue": S, "UnsignedAttributes OPTIONAL":{"OBJECT IDENTIFIER": "NULL", "SET OF AttributeValue": "NULL"}}}
        with open(name + ".json", "w", encoding="utf-8") as file:
            json.dump(c_m, file)
        c_m = self.ping_server(name)
        if c_m == 1:
            print("Signature is incorrect")
            return 0
        if self.Provreka(c_m):
            with open(name + ".json", "w", encoding="utf-8") as file:
                json.dump(c_m, file, indent=4)


    def Provreka(self, c_m):
        type_hesh = c_m['DigestAlgorithmIdentifiers']
        M = c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["User Signature"]
        t = c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["Timestamp Center Data"]["Timestamp Center Signature"]["t"]
        s = c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["Timestamp Center Data"]["Timestamp Center Signature"]["s"]
        b = c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["Timestamp Center Certificate"]["SubjectPublicKeyInfo"]["publicExponent"]
        n = c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["Timestamp Center Certificate"]["SubjectPublicKeyInfo"]["N"]

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
            c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["User Signature"] = hex(int(c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["User Signature"], 2))[2:]
            return True
        else:
            print("Signature is incorrect")
            return False


    def ping_server(self, name):
        url = 'http://localhost:8080'

        fp = open(name + ".json", 'rb')
        files = {"file": fp}

        resp = requests.post(url, files=files)
        fp.close()

        b = resp.text
        a = json.loads(b.replace("'", '"'))

        if resp:
            print('Response OK')
        else:
            print('Response Failed')

        return a


if __name__ == '__main__':
    obj = FSH()
    flag1 = input("Метод хеширования:\n1)Стрибог\n2)SHA\n")
    flag2 = input("Свертка:\n1)512 бит\n2)256 бит\n")
    obj.coding(flag1, flag2)