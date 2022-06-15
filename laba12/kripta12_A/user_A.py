import server

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import random
import requests
import json
import threading

class Authentication:
    def __init__(self):
        self.id_user = 756569485618495161487451564851648956148456214898562148956214895864185612
        self.stamp_a = 0

    def gen_key(self):
        key = get_random_bytes(16)

        self.p_GET(key)

        file_key = open("key.bin", "wb")
        file_key.write(key)
        file_key.close()

    def generate_random_string(self, length):
        import string
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string

    def coding(self, stamp_b):
        if input("Ввод M1:\n1)С клавиатуры\n2)Случайный набор символов\nВыбор:") == "1":
            M1 = input("Введите сообщение M1:")
        else:
            M1 = self.generate_random_string(random.randint(1, 1000))
        M2 = input("Введите сообщение:")

        messege = str({"stamp": {"user B":stamp_b, "user A": int(open('stamp_a.txt', 'r', encoding='utf-8').read())}, "id_user": self.id_user, "Messege": M1})
        data = bytes(messege, encoding='ascii')
        key = open("key.bin", "rb").read()

        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        Mes_test = b'3' + b'||' + M2.encode('ascii') + b'||' + cipher.nonce + b'||' + tag + b'||' + ciphertext
        self.p_POST(Mes_test)

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
                int(text["stamp"]["user A"]) == int(open('stamp_a.txt', 'r', encoding='utf-8').read()):
            print(f"User sent you a message:{Mes}")
            self.coding(text["stamp"]["user B"])
        else:
            print("User not authenticated.")

    def Stage_1(self):
        M2 = input("Введите сообщение:")

        stamp = random.randint(1, 9999999999999999999999999999)

        open('stamp_a.txt', 'w', encoding='utf-8').write(str(stamp))

        Mes_test = b'1' + b'||' + M2.encode('ascii') + b'||' + str(stamp).encode('ascii')
        t1 = threading.Thread(target=self.p_POST, args=[Mes_test])
        t1.start()
        t2 = threading.Thread(target=server.run())
        t2.start()

    def Stage_3(self, Mes):
        self.decoding(Mes)

    def p_POST(self, mes):
        url = 'http://localhost:8081'
        requests.post(url, data=mes)


    def p_GET(self, mes):
        url = 'http://localhost:8081'
        requests.put(url, data=mes)


if __name__ == '__main__':
    obj = Authentication()
    obj.gen_key()
    obj.Stage_1()