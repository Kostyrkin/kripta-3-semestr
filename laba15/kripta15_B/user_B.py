import requests
import json
import datetime
import random

class user():
    def save_and_gen_n(self):
        with open("Information_about_variables.json", "r", encoding='utf-8') as file:
            date = json.load(file)
        p = self.PMF(100, 100)
        q = self.PMF(100, 100)
        n = q * p
        date['n'] = int(n)
        with open("Information_about_variables.json", "w", encoding='utf-8') as file:
            json.dump(date, file, indent=4)
        return n

    def save_variables(self, Mes):
        with open("Information_about_variables.json", "r", encoding='utf-8') as file:
            date = json.load(file)
        date['v'] = int(Mes)
        with open("Information_about_variables.json", "w", encoding='utf-8') as file:
            json.dump(date, file, indent=4)


    def save_variables_it(self, Mes):
        with open("Information_about_variables.json", "r", encoding='utf-8') as file:
            date = json.load(file)
        if Mes[0] == "1":
            date['x'] = int(Mes[1:])
            c = random.randint(0, 1)
            date['c'] = c
            with open("Information_about_variables.json", "w", encoding='utf-8') as file:
                json.dump(date, file, indent=4)
            return c
        elif Mes[0] == "3":
            if int(Mes[1:]) != 0 and pow(int(Mes[1:]), 2, date['n']) == pow((date['x']*pow(date['v'], date['c'])), 1, date['n']):
                return 1
            else:
                return 0

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



