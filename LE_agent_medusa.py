from http.server import BaseHTTPRequestHandler,HTTPServer
import requests
from socketserver import ThreadingMixIn
import os,time
import logging

os.system('rm /home/ubuntu/vrp.log')
logging.basicConfig(filename="/home/ubuntu/vrp.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
vrp_port = 80
origin_ip = "daniele-mcom.s3.eu-central-1.amazonaws.com"

class ProxyHTTPRequestHandler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    def do_HEAD(self):
        self.do_GET(body=False)
    def do_GET(self, body=True):
        u1 = 'https://' + origin_ip + self.path
        resp = requests.get(u1)
        data = resp.content
        logger.debug("medusa:" + u1 + " IP: " + self.client_address[0] + ' time: ' + str(time.time()))
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)
        self.finish()
        return

    def handle(self):
        try:
            BaseHTTPRequestHandler.handle(self)
        except Exception as e:  # socket.error:
            if str(e) != 'I/O operation on closed file.':
                print(e)
            pass
# --------------------------------------------------------------------------
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass
    """Handle requests in a separate thread."""
# --------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        server_address = ('', vrp_port)
        server = ThreadedHTTPServer(server_address, ProxyHTTPRequestHandler)
        server.socket.settimeout(50)
        server.serve_forever()
    except Exception as e:
        print(str(e))


