import random
import json
import requests

import SHA
import Stribog


class AG:
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
        d = b2
        return m, d
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

    def C_AG(self):
        n = 100
        p = self.PMF(n, 100)
        a = random.randint(1, p - 2)
        while True:
            af = self.PMF(random.randint(3, n), 100)
            if pow(int(af), 2, int(p)) != 1 and pow(int(af), int((p-1)/2), int(p)) != 1 and int(af) < int(p):
                break
        b = pow(af, a, p)

        SubjectPublicKeyInfo = {"alpha": af, "beta": b, "p": p}
        p_k = {"SubjectPublicKeyInfo": SubjectPublicKeyInfo, "PKCS10CertRequest":"NULL", "Certificate":"NULL", "PKCS7CertChain-PKCS":"NULL"}
        with open("ok_AG.json", "w", encoding="utf-8") as file:
            json.dump(p_k, file, indent=4)

        c_k = {"privateExponent": a}
        with open("zk_AG.json", "w", encoding="utf-8") as file:
            json.dump(c_k, file, indent=4)

    def coding(self, Met, Sv):
        self.C_AG()
        with open("ok_AG.json", "r", encoding="utf-8") as file:
            p_k = json.load(file)
        with open("zk_AG.json", "r", encoding="utf-8") as file:
            c_k = json.load(file)
        a = c_k["privateExponent"]
        af = p_k["SubjectPublicKeyInfo"]["alpha"]
        p = p_k["SubjectPublicKeyInfo"]["p"]
        A = ["512", "256"]
        B = ["GOST", "SHA"]
        Mes = input("Введите сообщение:")
        M = self.mod_text_in_bit(Mes)
        if Met == "1":
            M = Stribog.heshf().hesh_function(M, Sv)
        else:
            M = SHA.SHA().SHA_function(M, Sv)
        # 1 этап
        while True:
            r = random.randint(1, p-2)
            m, fix = self.EA(r, p-1)
            if m == 1:
                break
        # 2 этап
        y = pow(af, r, p)
        # 3 этап
        m, r = self.EA((p-1), r)
        q = pow(((int(M, 2) - int(a)*int(y))*r), 1, int(p-1))
        # 4 этап
        S = {"y": hex(y)[2:], "q": hex(q)[2:]}

        c = B[int(Met) - 1] + A[int(Sv) - 1]
        name = input("Введите название файла для записи зашифровонного текста:")
        c_m = {"CMSVersion": 1, "DigestAlgorithmIdentifiers": c, "EncapsulatedContentInfo": {"ContentType": "text", "OCTET STRING OPTIONAL": Mes}, "CertificateSet OPTIONAL": p_k, "RevocationInfoChoises OPTIONAL":"NULL", "SignerInfos":{"CMSVersion":1, "SignerIdentifier":"Kostyrkin Nikita", "DigestAlgorithmIdentifier": c, "SignedAttributes OPTIONAL": "NULL", "SignatureAlgorithmIdentifier": "DSAdsi", "SignatureValue": S, "UnsignedAttributes OPTIONAL":{"OBJECT IDENTIFIER": "NULL", "SET OF AttributeValue": "NULL"}}}
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
        af = c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["Timestamp Center Certificate"]["SubjectPublicKeyInfo"]["alpha"]
        M = c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["User Signature"]
        b = c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["Timestamp Center Certificate"]["SubjectPublicKeyInfo"]["beta"]
        y = int(c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["Timestamp Center Data"]["Timestamp Center Signature"]["y"])
        p = c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["Timestamp Center Certificate"]["SubjectPublicKeyInfo"]["p"]
        q = int(c_m["SignerInfos"]["UnsignedAttributes OPTIONAL"]["SET OF AttributeValue"]["Timestamp Center Data"]["Timestamp Center Signature"]["q"])
        ah = pow(af, int(M, 2), p)
        by = pow(pow(b, y, p) * pow(y, q, p), 1, p)
        if by == ah:
            print("Signature is correct")
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
    obj = AG()
    flag1 = input("Метод хеширования:\n1)Стрибог\n2)SHA\n")
    flag2 = input("Свертка:\n1)512 бит\n2)256 бит\n")
    obj.coding(flag1, flag2)
