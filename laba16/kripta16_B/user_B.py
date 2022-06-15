import datetime
import random
import requests
import json
import RSA
import RSA_S


class Authentication:
    def __init__(self):
        self.id_user = 561320351351023156320325245312065178634605104631565265012650156156156010

    def coding(self,Messege):
        per = json.loads(RSA.RSA().decoding(Messege).replace("'", '"'))
        if RSA_S.RSA().Provreka(per, self.id_user):
            with open("info_test.json", "w", encoding="utf-8") as file:
                json.dump(per, file, indent=4)
            print(per['SessionKey'])
        #print(RSA.RSA().decoding(Messege))