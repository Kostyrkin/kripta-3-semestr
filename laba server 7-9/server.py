from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import json
import logging

import RSA
import AlGamal
import FSH


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def Proverka(self, b):
        self.c_m = json.loads(b.replace("'", '"'))

        UTC = datetime.datetime.now().strftime("%Y%m%d%I%M%S")
        GMT = datetime.datetime.utcnow().strftime("%Y%m%d%I%M%S")
        timestamp = {"UTC": UTC, "GMT": GMT}

        type_hesh = self.c_m['DigestAlgorithmIdentifiers']
        M = self.c_m['EncapsulatedContentInfo']['OCTET STRING OPTIONAL']
        hesh = self.c_m['SignerInfos']['SignatureValue']
        time = bin(int(timestamp["GMT"]))[2:].zfill(48) + bin(int(timestamp["UTC"]))[2:].zfill(48)

        self._set_response()
        if self.c_m['SignerInfos']["SignatureAlgorithmIdentifier"] == "RSAdsi":
            if RSA.RSA().Provreka_h(self.c_m):
                return False
            else:
                A, S_A = RSA.RSA().coding(M, hesh, time, type_hesh)
                with open("ok_RSA.json", "r", encoding="utf-8") as file:
                    p_k = json.load(file)
        elif self.c_m['SignerInfos']["SignatureAlgorithmIdentifier"] == "DSAdsi":
            if AlGamal.AG().Provreka_h(self.c_m):
                return False
            else:
                A, S_A = AlGamal.AG().coding(M, hesh, time, type_hesh)
                with open("ok_AG.json", "r", encoding="utf-8") as file:
                    p_k = json.load(file)
        elif self.c_m['SignerInfos']["SignatureAlgorithmIdentifier"] == "FSAdsi":
            if FSH.FSH().Provreka_h(self.c_m):
                return False
            else:
                A, S_A = FSH.FSH().coding(M, hesh, time, type_hesh)
                with open("ok_FSH.json", "r", encoding="utf-8") as file:
                    p_k = json.load(file)

        Set_Of_AttributeValue = {"User Signature": A, "timestamp": timestamp,
                "Timestamp Center Data": {"Timestamp Center Signature": S_A, "timestamp": timestamp},
                "Timestamp Center Certificate": p_k}

        self.c_m['SignerInfos']['UnsignedAttributes OPTIONAL']['OBJECT IDENTIFIER'] = "signature-time-stamp"
        self.c_m['SignerInfos']['UnsignedAttributes OPTIONAL']['SET OF AttributeValue'] = Set_Of_AttributeValue

        return True


    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        if self.Proverka(post_data.decode('utf-8').split("\n")[3]):
            self.wfile.write(str(self.c_m).encode('utf-8'))
        else:
            self.wfile.write("1".encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()