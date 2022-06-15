from http.server import BaseHTTPRequestHandler, HTTPServer
import user_B
import logging
import time
import threading

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
        post_data = self.rfile.read(content_length)

        self._set_response()
        time.sleep(1)
        Mes = post_data.split(b'||')
        if Mes[0] == b'1':
            t1 = threading.Thread(target=user_B.Authentication().Stage_2, args=[Mes[2].decode('ascii')])
            t1.start()
        elif Mes[0] == b'3':
            user_B.Authentication().Stage_4(Mes)
            raise KeyboardInterrupt


    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        self._set_response()
        self.save_key(post_data)

    def save_key(self, key):
        file_out = open("key.bin", "wb")
        file_out.write(key)
        file_out.close()

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