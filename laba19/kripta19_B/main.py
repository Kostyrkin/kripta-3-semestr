import json
import requests

def create_seans_key():
    url = 'http://localhost:8000'
    req = requests.get(url=url)
    r = int(req.text)
    g_p = json.load(open("params_g.json", "r", encoding="utf-8"))

    seans_key = 0
    step = 0
    for i in g_p:
        seans_key += i * pow(r, step)
        step += 1
    print(seans_key)

create_seans_key()