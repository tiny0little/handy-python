#!/usr/bin/python3.8

import socketserver

VERSION = '0.0.1'
nodes = []


class MyTCPClientHandler(socketserver.StreamRequestHandler):
    timeout = 60

    def handle(self):
        while True:
            self.wfile.write(str.encode("> "))
            msg = self.rfile.readline().strip()
            result = ""
            msg = msg.lower()

            if b'quit' in msg:
                break

            elif b'ver' in msg:
                result = VERSION

            elif b'help' in msg:
                result = "KNOWN COMMANDS ARE\nver help quit"

            else:
                result = "UNKNOWN COMMAND"

            result += "\n"
            self.wfile.write(str.encode(result))


TCPServerInstance = socketserver.ThreadingTCPServer(("127.0.0.1", 12345), MyTCPClientHandler)
TCPServerInstance.serve_forever()
