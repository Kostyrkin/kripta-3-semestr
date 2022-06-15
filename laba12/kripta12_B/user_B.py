from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import datetime
import random
import requests
import json

class Authentication:
    def __init__(self):
        self.id_user = 561320351351023156320325245312065178634605104631565265012650156156156010
        self.stamp_a = 0
        self.stamp_b = 0

    def generate_random_string(self, length):
        import string
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string

    def decoding(self, Messege):
        nonce = Messege[2]
        ciphertext = Messege[4]
        tag = Messege[3]
        Mes = Messege[1].decode('ascii')

        key = open("key.bin", "rb").read()

        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)

        text = json.loads(data.decode('ascii').replace("'", '"'))
        if int(text["id_user"]) in json.loads(open('user.json', 'r', encoding='utf-8').read()) and \
                int(text["stamp"]["user A"]) == int(open('stamp_a.txt', 'r', encoding='utf-8').read()) and \
                int(text["stamp"]["user B"]) == int(open('stamp_b.txt', 'r', encoding='utf-8').read()):
            print(f"User sent you a message:{Mes}")
        else:
            print("User not authenticated.")

    def p_POST(self, mes):
        url = 'http://localhost:8080'
        requests.post(url, data=mes)

    def p_GET(self, mes):
        url = 'http://localhost:8080'
        requests.put(url, data=mes)

    def Stage_2(self, stamp_a):
        if input("Ввод M1:\n1)С клавиатуры\n2)Случайный набор символов\nВыбор:") == "1":
            M1 = input("Введите сообщение M1:")
        else:
            M1 = self.generate_random_string(random.randint(1, 1000))
        M2 = input("Введите сообщение:")

        stamp_b = random.randint(1, 9999999999999999999999999999)

        open('stamp_a.txt', 'w', encoding='utf-8').write(str(stamp_a))
        open('stamp_b.txt', 'w', encoding='utf-8').write(str(stamp_b))

        messege = str({"stamp": {"user A":stamp_a, "user B": stamp_b}, "id_user": self.id_user, "Messege": M1})
        data = bytes(messege, encoding='ascii')
        key = open("key.bin", "rb").read()

        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        Mes_test = b'2' + b'||' + M2.encode('ascii') + b'||' + cipher.nonce + b'||' + tag + b'||' + ciphertext
        self.p_POST(Mes_test)

    def Stage_4(self, Mes):
        self.decoding(Mes)