import server
import RSA
import SHA
import Stribog

import datetime
import random
import requests
import json
import threading

class Authentication:
    def __init__(self):
        self.id_user = 756569485618495161487451564851648956148456214898562148956214895864185612

    def gen_key(self):
        key = RSA.RSA().C_RSA()

        self.p_POST('key_ided',key)

    def coding(self):
        z = random.randint(1, 9461894568948165946532)
        open('stamp.txt','w',encoding='utf-8').write(str(z))
        Met = input("Метод хеширования:\n1)Стрибог\n2)SHA\n")
        Sv = input("Свертка:\n1)512 бит\n2)256 бит\n")
        if Met == "1":
            Hz = Stribog.heshf().hesh_function(bin(z)[2:], Sv)
        else:
            Hz = SHA.SHA().SHA_function(bin(z)[2:], Sv)

        with open("zk_identification.json", "r", encoding="utf-8") as file:
            z_k = json.load(file)

        Mes = RSA.RSA().coding(Met, Sv, "0"*(8 - (len(bin(z)[2:] + bin(self.id_user)[2:]) % 8)) + bin(z)[2:] + bin(self.id_user)[2:], z_k, "zk")

        Mes_test = {'hesh': Hz, 'id_user': self.id_user, 'enc_messege': Mes}
        t1 = threading.Thread(target=self.p_POST, args=['body_ided', Mes_test])
        t1.start()
        t2 = threading.Thread(target=server.run())
        t2.start()

    def decoding(self, z):
        if z == open('stamp.txt', 'r', encoding='utf-8').read():
            open('ided.txt', 'w', encoding='utf-8').write("True")
        else:
            open('ided.txt', 'w', encoding='utf-8').write("False")

    def p_POST(self, indef, mes):
        url = 'http://localhost:8081'

        requests.post(url, params=indef, json=mes)

def identification():
    obj = Authentication()
    obj.gen_key()
    obj.coding()