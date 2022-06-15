import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

import json
import datetime
import random

import user_B

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/vnd.ms-excel')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        Mes = str(user_B.user().save_and_gen_n())
        self.save_info(Mes)
        self.wfile.write(Mes.encode('utf-8'))


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        self._set_response()
        self.save_info(post_data)
        if post_data[0] == "0":
            user_B.user().save_variables(post_data[1:])
        elif post_data[0] == "1":
            c = str(user_B.user().save_variables_it(post_data))
            self.save_info(c, True)
            self.wfile.write(c.encode('utf-8'))
        elif post_data[0] == "3":
            met = str(user_B.user().save_variables_it(post_data))
            self.save_info(met, True)
            self.wfile.write(met.encode('utf-8'))
        elif post_data == "True":
            print('User identified')
            raise KeyboardInterrupt

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        self._set_response()

    def save_info(self, Mes, flag=False):
        with open("date_info.json", "r", encoding='utf-8') as file:
            date = json.load(file)
        if flag:
            date["SentMessage"][str(datetime.datetime.now())] = Mes
        else:
            date["ReceivedMessage"][str(datetime.datetime.now())] = Mes
        with open("date_info.json", "w", encoding='utf-8') as file:
            json.dump(date, file, indent=4)

def run(server_class=HTTPServer, handler_class=S, port=8081):
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

