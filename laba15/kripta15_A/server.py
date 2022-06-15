import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


import datetime

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/vnd.ms-excel')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        self._set_response()
        """info = json.loads(json.loads(post_data))

        if info['Action'] == "GOTK":
            text = GOP.GOTK(info)
        elif info['Action'] == "IDN":
            text = GOP.IDN(info)

        self.wfile.write(json.dumps(text).encode('utf-8'))"""

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

