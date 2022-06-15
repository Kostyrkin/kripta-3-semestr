import json
import Stribog
import SHA


def GOTK(Mes): #Generation of one-time keys
    s_txt = {'id': Mes['IDUser'], 'hesh': Mes['HashMethod'], 'key': Mes['HeshPassword']}
    if save_file(s_txt):
        return "1"
    else:
        return "0"

def save_file(save):
    with open("date_user.json", "r", encoding='utf-8') as file:
        users = json.load(file)
    if str(save['id']) in users["User"]:
        if users["User"][str(save['id'])]['NumberOfIterations'] == 11:
            users["User"][str(save['id'])] = {'NumberOfIterations': 1, 'HashMethod': save['hesh'],
                                              'DisposableKeys': save['key']}
            with open("date_user.json", "w", encoding='utf-8') as file:
                json.dump(users, file, indent=4)
        else:
            print("User already registered")
            return False
    else:
        users["User"][str(save['id'])] = {'NumberOfIterations': 1, 'HashMethod': save['hesh'], 'DisposableKeys': save['key']}
        with open("date_user.json", "w", encoding='utf-8') as file:
            json.dump(users, file, indent=4)
        print("User registered")
        return True

def IDN(Mes):
    with open("date_user.json", "r", encoding='utf-8') as file:
        users = json.load(file)
    if str(Mes['IDUser']) in users["User"]:
        if Mes["NumberOfIterations"] == users["User"][str(Mes['IDUser'])]["NumberOfIterations"]:
            metod = users["User"][str(Mes['IDUser'])]['HashMethod']
            it = users["User"][str(Mes['IDUser'])]['NumberOfIterations']
            H = users["User"][str(Mes['IDUser'])]['DisposableKeys']
            od_key = Mes['DisposableKeys']

            if metod == "GOST512":
                H_p = Stribog.heshf().hesh_function(od_key, "1")
            elif metod == "GOST256":
                H_p = Stribog.heshf().hesh_function(od_key, "2")
            elif metod == "SHA512":
                H_p = SHA.SHA().SHA_function(od_key, "1")
            elif metod == "SHA256":
                H_p = SHA.SHA().SHA_function(od_key, "2")

            if H == H_p:
                users["User"][str(Mes['IDUser'])]['NumberOfIterations'] = it + 1
                users["User"][str(Mes['IDUser'])]['DisposableKeys'] = od_key
                with open("date_user.json", "w", encoding='utf-8') as file:
                    json.dump(users, file, indent=4)
                return "5"
            else:
                return "4"
        else:
            return "3"
    else:
        return "2"

"""
1 - Пользователь зарегестрирован
2 - Неопознанный id пользователя
3 - Неверная итерация запроса
4 - Неверный одноразовый пароль
5 - Пользователь индифецирован
"""