#! -*- coding:utf-8 -*-
#!/usr/bin/python
from  BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import ssl


class HTTPSHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print '----------  %s  ----------' % self.log_date_time_string()
        print self.requestline
        for i in self.headers.headers:
            print i.strip()


def main():
    try:
        server=HTTPServer(('ip',4443),HTTPSHandler)
        server.socket = ssl.wrap_socket(server.socket, certfile='./server.pem', server_side=True)
        server.serve_forever()
    except KeyboardInterrupt:
        print '[!] Server Shut Down.'
        server.socket.close()


if  __name__=='__main__':
    main()
