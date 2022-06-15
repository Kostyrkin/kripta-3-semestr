import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import FSH


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_response()
        with open("object.json", "r", encoding="utf-8") as file:
            self.wfile.write(json.dumps(json.load(file)["P"]).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        self._set_response()
        if self.path[2:] == "Key":
            info = json.loads(post_data)
            FSH.GP().C_GP(info)
        elif self.path[2:] == "Stage1":
            self.wfile.write(str(FSH.GP().Stage1(post_data)).encode('utf-8'))
        elif self.path[2:] == "Stage2":
            self.wfile.write(str(FSH.GP().Stage2(post_data)).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8000):
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