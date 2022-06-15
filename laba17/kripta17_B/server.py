from http.server import BaseHTTPRequestHandler, HTTPServer
import Identification
import PDH
import PSK
import RSA
import logging
import time
import json


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/vnd.ms-excel')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write(json.dumps(RSA.RSA().C_RSA("ok_PSK.json", "zk_PSK.json")).encode('utf-8'))


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        self._set_response()
        time.sleep(1)
        if self.path[2:] == 'key_ided':
            post_data = json.loads(post_data.replace("'", '"'))
            with open("ok_identification .json", "w", encoding="utf-8") as file:
                json.dump(post_data, file)
        elif self.path[2:] == 'body_ided':
            post_data = json.loads(post_data.replace("'", '"'))
            Identification.Authentication().coding(post_data)
        elif self.path[2:] == 'PSK':
            post_data = json.loads(post_data.replace("'", '"'))
            PSK.Authentication().coding(post_data)
        elif self.path[2:] == 'alfa':
            self.wfile.write(PDH.PDH().main(post_data).encode('utf-8'))
            raise KeyboardInterrupt

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