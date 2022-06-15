import random
import json
import requests

import SHA
import Stribog


class GP:
    def __init__(self):
        pass

    # Euclid's algorithm(алгорим Евклида)
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
        b = b2
        return m, b
        # d=a a=u b=v au + bv = gcd(a, b).

    def save_object(self, name, obj):
        with open("object.json", "r", encoding='utf-8') as file:
            mas = json.load(file)
        mas[name] = obj
        with open("object.json", "w", encoding='utf-8') as file:
            json.dump(mas, file, indent=4)

    # Cipher RSA(Шифр RSA)
    def C_GP(self, info):
        self.save_object("p", info["p"])
        self.save_object("q", info["q"])
        self.save_object("alfa", info["alfa"])

        k = random.randint(1, info["p"] - 1)
        P = pow(info["alfa"], k, info["p"])
        self.save_object("k", k)
        self.save_object("P", P)

    def Stage1(self, lb):
        self.save_object("lambda", int(lb))
        with open("object.json", "r", encoding="utf-8") as file:
            info = json.load(file)

        t = random.randint(1, info["q"])
        self.save_object("t", int(t))
        R = pow(info["alfa"], t, info["p"])
        self.save_object("R", int(R))
        return R

    def Stage2(self, E):
        self.save_object("E", int(E))
        with open("object.json", "r", encoding="utf-8") as file:
            info = json.load(file)
        S = pow((info["t"] + info["k"]*info["lambda"]*int(E)), 1, info["q"])
        self.save_object("S", int(S))
        return S
