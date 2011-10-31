import SocketServer
import socket
import struct
import random

'''
NOTE: 
Jar system fuer AES verschluesselte Dateien:
Wir muessen um unsere zu transportierenden Daten
sicher und verlustfrei zu uebertragen einen container
um die rohdaten wrappen, welcher einen header der eigentlichen
Datei enthaelt. Das bedeutet: Name der Datei, Groesse der Datei,
Von wem zu wem, etc.
Danach wird mit \x00 aufgefuellt bis der container durch 16
teilbar ist.
'''

class common(object):
    def recvData(self, addr, filesize):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            port = random.randint(49152, 65535)
            print port
            sock.bind(("", int(port)))
            sock.connect((addr, int(port)))
            data = sock.recv(filesize)
    
        except Exception as msg:
            print msg
            common().recvData(addr, filesize)

        return data


class communicator(SocketServer.BaseRequestHandler):
# write this crap with select on socket
    def handle(self):
        # struct which inits: "!6sI" == "IIINIT", unsigned int [Filesize]
        inputRequest, addr = self.request.recvfrom(10)
        init, filesize = struct.unpack("!6sI", inputRequest)
        print init, filesize
        data = common().recvData(addr, filesize)
        print "done"
        return 0
        # TODO: Encrypt data
        # TODO: Serialize data and pipe it to display or message etc
        


class scream(object):
    def call(self):
        HOST, PORT = "localhost", 9616
        server = SocketServer.TCPServer((HOST, PORT), communicator)
        server.serve_forever()