import json
import random
import requests


def gen_key():
    F = 133266086983106976272640155790060239821588811044472717882577392317552341387300944980553973742646154241432077459593531556297512039015000892778393370354443026238371710847929474381653077900079146299467973679198551204893042192811325553476803879377971110110640520554603401118999077811601693770382086333652995021159
    n = 2
    r = []
    for i in range(n):
        r.append(random.randint(1, F))
    print(r)
    for i in range(n):
        url = 'http://localhost:8' + str(i).zfill(4 - len(str(i)))
        req = requests.post(url=url, params="P_r", data=str(r[i]))

    m = random.randint(1, n)
    f_xy = []
    for i in range(m+1):
        for j in range(m+1):
            if j < i:
                a = f_xy[(m+1)*j+i][0]
            else:
                a = random.randint(1, F)
            f_xy.append([a, i, j])

    with open("function_params.json", "w", encoding="utf-8") as file:
        json.dump(f_xy, file)

    g_p = []
    for k in range(n):
        g_p.append([])
        for i in range(m+1):
            sum = 0
            for j in range(m+1):
                sum += f_xy[(m+1)*j+i][0]*pow(r[k], f_xy[(m+1)*j+i][1])
            g_p[k].append(sum)

    for i in range(n):
        url = 'http://localhost:8' + str(i).zfill(4 - len(str(i)))
        req = requests.post(url=url, params="P_g", json=g_p[i])

    stroka_f = ""
    for i in f_xy:
        stroka_f += f"{i[0]}*x^{i[1]}*y^{i[2]}||"
    print(stroka_f)
    print(g_p)
    #проверка
    """sum_f = 0
    for i in f_xy:
        sum_f +=i[0]*pow(r[0], i[1])*pow(r[1], i[2])
    print(sum_f)
    sum_p_a = 0
    step = 0
    for i in g_p[0]:
        sum_p_a += i*pow(r[1], step)
        step += 1
    print(sum_p_a)
    if sum_f == sum_p_a:
        print(True)"""

gen_key()
