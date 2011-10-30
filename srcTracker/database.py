import sqlite3
import SocketServer

class connection(SocketServer.BaseRequestHandler):

# packet contains: username, password (hash)

    def handle(self):
        addr = self.client_address[0]
        while 1:
            # just a small struct
            packet = self.request.recv(512)
            # TODO: extract data from packet
            if packet:
                return packet
            else:
                return struct.pack("!%ss" % (len(addr)), addr)
            