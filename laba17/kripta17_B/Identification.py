import datetime
import random
import requests
import json

class Authentication:
    def __init__(self):
        self.id_user = 561320351351023156320325245312065178634605104631565265012650156156156010

    def generate_random_string(self, length):
        import string
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(length))
        return rand_string

    def coding(self,Messege):
        import RSA
        import SHA
        import Stribog

        with open("ok_identification .json", "r", encoding="utf-8") as file:
            p_k = json.load(file)

        Mes = RSA.RSA().decoding(Messege['enc_messege']['EncryptedContentInfo']['encryptedContent'], p_k, "ok")

        z = str(int(Mes))[:-len(bin(Messege['id_user'])[2:])]
        type_hesh = Messege['enc_messege']['EncryptedContentInfo']['OPTIONAL']['DigestAlgorithmIdentifiers']

        if type_hesh == "GOST512":
            Hz = Stribog.heshf().hesh_function(z, "1")
        elif type_hesh == "GOST256":
            Hz = Stribog.heshf().hesh_function(z, "2")
        elif type_hesh == "SHA512":
            Hz = SHA.SHA().SHA_function(z, "1")
        elif type_hesh == "SHA256":
            Hz = SHA.SHA().SHA_function(z, "2")

        if Hz == Messege['hesh']:
            if Messege["id_user"] in json.loads(open('user.json', 'r', encoding='utf-8').read()):
                print("User identified")
                open('ided.txt', 'w', encoding='utf-8').write("True")
                self.p_POST(str(int(z, 2)))
            else:
                print('User not identified')
                open('ided.txt', 'w', encoding='utf-8').write("False")
                self.p_POST(0)

    def decoding(self, Messege):
        pass

    def p_POST(self, mes):
        url = 'http://localhost:8080'

        resp = requests.post(url, data=mes)