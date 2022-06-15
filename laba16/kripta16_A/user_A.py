import RSA
import RSA_S

import datetime
import random
import requests
import json

class Authentication:
    def __init__(self):
        self.id_user = 756569485618495161487451564851648956148456214898562148956214895864185612

    def gen_key(self):
        url = 'http://localhost:8081'
        req = requests.get(url, data="key")

        with open("ok_os_B.json", 'w', encoding='utf-8') as file:
            json.dump(json.loads(req.text), file)

    def GSK(self, length=256):
        mas = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
        rand_key = ''
        for i in range(length):
            rand_key = rand_key + mas[random.randint(0,15)]
        return rand_key

    def mod_text_in_bin(self, text: str) -> str:
        bit_text = ''
        encode_text = text.encode('utf-8')
        for i in range(len(encode_text)):
            bit_text = bit_text + '0' * (8 - len(format(encode_text[i], 'b'))) + format(encode_text[i], 'b')
        return bit_text

    def coding(self):
        session_key = self.GSK()
        print(session_key)
        UTC = datetime.datetime.now().strftime("%Y%m%d%I%M%S")
        GMT = datetime.datetime.utcnow().strftime("%Y%m%d%I%M%S")
        timestamp = GMT + UTC
        with open("date_user.json", "r", encoding='utf-8') as file:
            id_B = json.load(file)['user_B']
        M = self.mod_text_in_bin(str({"IDUser": id_B, "SessionKey":session_key, "TimeStamp": timestamp}))
        S_user_A = RSA_S.RSA().coding("2", "1", M)
        Mes = self.mod_text_in_bin(str({'SessionKey': session_key, "TimeStamp": timestamp, "DigitalSignature": S_user_A}))
        C_Messege = RSA.RSA().coding(Mes)
        #print(RSA.RSA().decoding(C_Messege))
        self.p_POST(C_Messege)


    def p_POST(self, mes):
        url = 'http://localhost:8081'
        requests.post(url, json=mes)

if __name__ == '__main__':
    obj = Authentication()
    obj.gen_key()
    obj.coding()