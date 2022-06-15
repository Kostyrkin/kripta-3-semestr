import json
import random

class PDH:
    def main(self, Mes):
        if open('ided.txt', 'r', encoding='utf-8').read() == "True":
            with open("object.json", "r", encoding='utf-8') as file:
                mas = json.load(file)
            self.save_object("alfa", int(Mes))
            y = random.randint(2, mas["p"] - 2)
            self.save_object("y", y)
            bt = pow(mas["g"], y, mas["p"])
            self.save_object("betta", bt)
            k = pow(int(Mes), y, mas["p"])
            self.save_object("k", k)
            return str(bt)
        else:
            print('User not identified')

    def save_object(self, name, obj):
        with open("object.json", "r", encoding='utf-8') as file:
            mas = json.load(file)
        mas[name] = obj
        with open("object.json", "w", encoding='utf-8') as file:
            json.dump(mas, file, indent=4)