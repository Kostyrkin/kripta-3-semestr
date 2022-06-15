import requests
import json

import SHA
import Stribog

class inditification():
    def __init__(self):
        self.id_user = 756569485618495161487451564851648956148456214898562148956214895864185612

    def registr(self):
        A = ["GOST", "SHA"]
        B = ["512", "256"]
        Hmt = A[int(input("Метод хеширования:\n1)Стрибог\n2)SHA\nВыбор:"))-1] + B[int(input("Длина хеша:\n1)512 бит\n2)256 бит\nВыбор:"))-1]
        secret_password = (input("Введите секретный пароль:"))
        sb = self.mod_text_in_bit(secret_password)

        n = 10

        H = sb
        for i in range(n):
            if Hmt == "GOST512":
                H = Stribog.heshf().hesh_function(H, "1")
            elif Hmt == "GOST256":
                H = Stribog.heshf().hesh_function(H, "2")
            elif Hmt == "SHA512":
                H = SHA.SHA().SHA_function(H, "1")
            elif Hmt == "SHA256":
                H = SHA.SHA().SHA_function(H, "2")


        Mes = {'Action': "GOTK", 'HashMethod': Hmt, "IDUser": self.id_user,
               'HeshPassword': H}

        with open('disposable_keys.json', 'w', encoding='utf-8') as file:
            key = {'NumberOfIterations':1, 'HashMethod': Hmt, 'SecretPassword': secret_password}
            json.dump(key, file, indent=4)

        ot_ser = self.ping_server(Mes)
        if int(ot_ser):
            print("You are registered")
        else:
            print("You have already been registered")

    def inditification(self):
        n = 10
        with open('disposable_keys.json', 'r', encoding='utf-8') as file:
            info = json.load(file)
        it = info['NumberOfIterations']
        Hmt = info['HashMethod']
        H = self.mod_text_in_bit(info['SecretPassword'])
        for i in range(n - it):
            if Hmt == "GOST512":
                H = Stribog.heshf().hesh_function(H, "1")
            elif Hmt == "GOST256":
                H = Stribog.heshf().hesh_function(H, "2")
            elif Hmt == "SHA512":
                H = SHA.SHA().SHA_function(H, "1")
            elif Hmt == "SHA256":
                H = SHA.SHA().SHA_function(H, "2")

        Mes = {'Action': "IDN", 'NumberOfIterations': it, "IDUser": self.id_user,
               'DisposableKeys': H}
        ot_ser = self.ping_server(Mes)
        if ot_ser == "2":
            print("Unrecognized user id")
        elif ot_ser == "3":
            print("Invalid query iteration")
        elif ot_ser == "4":
            print("Wrong one-time password")
        elif ot_ser == "6":
            print("One time password already used")
        elif ot_ser == "5":
            print("User is identified")
            info['NumberOfIterations'] = info['NumberOfIterations'] + 1
            with open('disposable_keys.json', 'w', encoding='utf-8') as file:
                json.dump(info, file, indent=4)

    def ping_server(self, Mes):
        url = 'http://localhost:8080'

        files = json.dumps(Mes)

        resp = requests.post(url, json=files)

        if len(resp.text) == 1:
            a = resp.text
        else:
            a = json.loads(resp.text)

        if resp:
            print('Response OK')
        else:
            print('Response Failed')

        return a

    def mod_text_in_bit(self, text: str) -> str:
        bit_text = ''
        encode_text = text.encode('utf-8')
        for i in range(len(encode_text)):
            bit_text = bit_text + '0' * (8 - len(format(encode_text[i], 'b'))) + format(encode_text[i], 'b')
        return bit_text
def run():
    with open('disposable_keys.json', 'r', encoding='utf-8') as file:
        info = json.load(file)
    if info['NumberOfIterations'] == 11:
        inditification().registr()
    inditification().inditification()

"""--------------------------------"""
run()