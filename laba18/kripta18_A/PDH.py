import json

import Identification
import PSK
import random
import requests
import GOP
import SHA


class PDH():
    def main(self):
        Identification.identification()
        if open('ided.txt', 'r', encoding='utf-8').read() == "True":
            print("User identified")
            p, g, k = self.gen_key(100)
            if input("Метод:\n1)Примитивынй элемент\n2)Одноразовый ключ\nВыбор:") == "2":
                if open("metka_GOP.txt", 'r', encoding='utf-8').read() == "False":
                    GOP.inditification().registr()
                    open('metka_GOP.txt', 'w', encoding='utf-8').write("True")
                w = GOP.run()
                if not w == "False":
                    g = pow(int(SHA.SHA().SHA_512(w), 2), 1, p)
                else:
                    return 0
            self.save_object("g", g)
            PSK.ran(p, g)
            x = random.randint(2, p-2)
            self.save_object("x", x)
            af = pow(g, x, p)
            self.save_object("alfa", af)
            bt = int(self.p_POST("alfa", af))
            self.save_object("betta", bt)
            k = pow(bt, x, p)
            self.save_object("k", k)
        else:
            print('User not identified')

    def save_object(self, name, obj):
        with open("object.json", "r", encoding='utf-8') as file:
            mas = json.load(file)
        mas[name] = obj
        with open("object.json", "w", encoding='utf-8') as file:
            json.dump(mas, file, indent=4)

    def gen_key(self, n=512):
        p = self.PMF(n, 100)
        self.save_object("p", p)
        k = self.GSK()
        self.save_object("k", k)
        while True:
            g = self.PMF(random.randint(3, n), 100)
            if pow(int(g), 2, int(p)) != 1 and pow(int(g), int((p - 1) / 2), int(p)) != 1 and int(g) < int(p):
                break
        return p, g, k

    def GSK(self, length=256):
        mas = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
        rand_key = ''
        for i in range(length):
            rand_key = rand_key + mas[random.randint(0,15)]
        return rand_key

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

    def p_POST(self, indef, mes):
        url = 'http://localhost:8081'

        req = requests.post(url, params=indef, json=mes)

        return req.text

if __name__ == '__main__':
    PDH().main()