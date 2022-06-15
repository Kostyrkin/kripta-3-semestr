import SHA
import Stribog
import random


def HMAC(Mes, Sver, Met):
    Opad, Ipad, K = gen_key(Sver, Met)
    M = mod_text_in_bit(Mes)
    K_O = ""
    for i in range(len(K)):
        K_O += str(int(K[i]) ^ int(Opad[i]))
    K_I = ""
    for i in range(len(K)):
        K_I += str(int(K[i]) ^ int(Ipad[i]))
    if Met == "1":
        return hex(int(Stribog.heshf().hesh_function(K_O + Stribog.heshf().hesh_function(K_I + M, Sver), Sver), 2))[2:]
    else:
        return hex(int(SHA.SHA().SHA_function(K_O + SHA.SHA().SHA_function(K_I + M, Sver), Sver), 2))[2:]

def mod_text_in_bit(text: str) -> str:
    bit_text = ''
    encode_text = text.encode('utf-8')
    for i in range(len(encode_text)):
        bit_text = bit_text + '0' * (8 - len(format(encode_text[i], 'b'))) + format(encode_text[i], 'b')
    return bit_text

def gen_key(Sver, Met):
    if Sver == "1" and Met == "2":
        b = 1024
    else:
        b = 512
    d = random.randint(0, 1000)
    key = ""
    for i in range(d):
        if random.randint(0, d) % 2 == 0:
            key += "0"
        else:
            key += "1"
    if len(key) < b:
        key = key + "0" * (b - len(key))
    else:
        key = key[:b]
    Ipad = "00110110" * int(b / 8)
    Opad = "01011100" * int(b / 8)
    with open("key.txt", "w", encoding="utf-8") as file:
        file.write(key)
    return Opad, Ipad, key

if __name__ == '__main__':
    if input("Сообщение:\n1)С консоли\n2)С файла\n") == "1":
        Mes = input("Тескт:")
    else:
        Mes = open(input("Введите путь к файлу:"), "r", encoding="utf-8").read()
    flag = input("Свертка:\n1)512 бит\n2)256 бит\n")
    flag1 = input("Метод хеширования:\n1)Стрибог\n2)SHA\n")
    Hmac = HMAC(Mes, flag, flag1)
    print(Hmac)
