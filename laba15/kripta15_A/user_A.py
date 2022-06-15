import requests
import json
import datetime
import random

class user():
    def inditification(self):
        n = int(self.get_n())
        while True:
            s = random.randint(2, n-1)
            m = self.EA(s, n)
            if m == 1:
                break
        v = pow(s, 2, n)
        self.ping_server("0" + str(v))
        # итерационный цикл
        for i in range(10):
            # 3.1
            print(i)
            z = random.randint(1, n-1)
            x = pow(z, 2, n)
            c = self.ping_server("1" + str(x))
            if c == "0":
                y = z
            else:
                y = pow((z*s), 1, n)
            """if y != 0 and pow(y, 2, n) == pow((x*pow(v,int(c))),1,n):
                print("Ok")"""
            met = int(self.ping_server("3" + str(y)))
            if not met:
                print("User not identified")
                return 0
        print("User identified")
        self.ping_server("True")

    def ping_server(self, Mes):
        url = 'http://localhost:8081'

        self.save_info(Mes, True)
        resp = requests.post(url, data=Mes)


        a = resp.text
        self.save_info(a)

        if resp:
            print('Response OK')
        else:
            print('Response Failed')

        return a

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
        return m

    def get_n(self):
        url = 'http://localhost:8081'

        resp = requests.get(url)

        a = resp.text
        self.save_info(a)

        if resp:
            print('Response OK')
        else:
            print('Response Failed')

        return a

    def save_info(self, Mes, flag=False):
        with open("date_info.json", "r", encoding='utf-8') as file:
            date = json.load(file)
        if flag:
            date["SentMessage"][str(datetime.datetime.now())] = Mes
        else:
            date["ReceivedMessage"][str(datetime.datetime.now())] = Mes
        with open("date_info.json", "w", encoding='utf-8') as file:
            json.dump(date, file, indent=4)

user().inditification()