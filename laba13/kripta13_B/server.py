from http.server import BaseHTTPRequestHandler, HTTPServer
import user_B
import logging
import time
import json


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
        post_data = json.loads(post_data.replace("'", '"'))
        time.sleep(1)
        if self.path[2:] == 'key':
            with open("zk_user.json", "w", encoding="utf-8") as file:
                json.dump(post_data, file)
        else:
            user_B.Authentication().coding(post_data)
            raise KeyboardInterrupt

    def save_key(self, key):
        file_out = open("zk_user.bin", "wb")
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