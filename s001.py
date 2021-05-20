#!/usr/bin/python3.8

import socketserver
import threading


class MyTCPClientHandler(socketserver.StreamRequestHandler):

    def handle(self):
        msg = self.rfile.readline().strip()
        result = ""
        # self.wfile.write(msg.upper())
        # print(f"Data Received from client is: {msg}")
        if b'ver' in msg:
            result = "0.0.1"

        self.wfile.write(str.encode(result))


TCPServerInstance = socketserver.ThreadingTCPServer(("127.0.0.1", 12345), MyTCPClientHandler)
TCPServerInstance.serve_forever()
