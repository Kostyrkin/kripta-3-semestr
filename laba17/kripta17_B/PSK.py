import datetime
import random
import requests
import json
import RSA
import RSA_S


class Authentication:
    def __init__(self):
        self.id_user = 561320351351023156320325245312065178634605104631565265012650156156156010

    def coding(self,Messege):
        with open("zk_PSK.json", "r", encoding='utf-8') as file:
            p_k = json.load(file)
        per = RSA.RSA().decoding(Messege["EncryptedContentInfo"]["encryptedContent"], p_k, "zk")
        slovo = ""
        for i in range(0, len(per), 8):
            slovo += bytes.fromhex(hex(int(per[i:i + 8], 2))[2:]).decode()
        per = json.loads(slovo.replace("'", '"'))
        if RSA_S.RSA().Provreka(per, self.id_user):
            self.save_object("p", per["p"])
            self.save_object("g", per["g"])

        #print(RSA.RSA().decoding(Messege))
    def save_object(self, name, obj):
        with open("object.json", "r", encoding='utf-8') as file:
            mas = json.load(file)
        mas[name] = obj
        with open("object.json", "w", encoding='utf-8') as file:
            json.dump(mas, file, indent=4)