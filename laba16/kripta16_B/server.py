from http.server import BaseHTTPRequestHandler, HTTPServer
import user_B
import logging
import time
import json

import RSA


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/vnd.ms-excel')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write(json.dumps(RSA.RSA().C_RSA()).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        self._set_response()
        post_data = json.loads(post_data)
        time.sleep(1)
        user_B.Authentication().coding(post_data)
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