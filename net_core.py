from lxml import html
import csv, os, json
import requests
from time import sleep
import urlparse2 as urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import _thread

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
        parsed_path = urlparse.urlparse(self.path)
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

    def do_HEAD(self):
        self._set_headers()


if __name__ == '__main__':
    server_address = ('', 1223)
    # scrap_core.__init__()
    httpd = HTTPServer(server_address, TestClass)
    # ixd = scrap_core.parseIDfromURL("https://www.amazon.in/dp/B00WMNXH7Q/ref=cm_sw_r_other_apa_i_Yv3KAbWJTEE0K")
    # scrap_core.addIDtoQueue(ixd)
    # scrap_core.BeginWorker()
    httpd.serve_forever()