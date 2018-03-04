from lxml import html
import csv, os, json
import requests
from time import sleep
from urllib import parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import _thread
import skrappy_01
import sys_core

rootDir = os.getcwd()


class TestClass(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def printStuff(self):
        print
        'Yo!'

    def do_GET(self):
        parsed_path = parse.urlparse(self.path)
        message_parts = []
        for name, value in sorted(self.headers.items()):
            self.printStuff()
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bytes(message,"utf-8"))
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #str(self.path), str(self.headers), post_data.decode('utf-8'))
        self._set_response()
        self.handle_POST()
        # self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        # self.wfile.write("\nPOST request with header {}".format(str(self.headers)).encode('utf-8'))
        # self.wfile.write("Body: {}".format(str(post_data.decode('utf-8'))).encode('utf-8'))

    def handle_POST(self):
        if self.path=="/queue":
            for name,value in self.headers.items():
                if name == "id":
                    x = skrappy_01.GetCurrentQueueFromId(value)
                    self.wfile.write(str(json.loads(json.dumps(x))).replace("'","\"").encode('utf-8'))
        elif self.path=="/add":
            uid=""
            url=""
            for name,value in self.headers.item():
                if name == "id":
                    uid=value
                elif name =="url":
                    url = value

            if(uid == "" or url == ""):
                return



    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def handleGet(self):
        return('yo')

def BeginNetCore():
    server_address=('',1441)
    httpd = HTTPServer(server_address,TestClass)
    httpd.serve_forever()

if __name__ == '__main__':
    _thread.start_new(BeginNetCore())
#     server_address = ('', 1223)
#     # scrap_core.__init__()
#     httpd = HTTPServer(server_address, TestClass)
#     # ixd = scrap_core.parseIDfromURL("https://www.amazon.in/dp/B00WMNXH7Q/ref=cm_sw_r_other_apa_i_Yv3KAbWJTEE0K")
#     # scrap_core.addIDtoQueue(ixd)
#     # scrap_core.BeginWorker()
#     httpd.serve_forever()