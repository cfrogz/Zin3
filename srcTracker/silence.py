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

class communicator(SocketServer.BaseRequestHandler):
    def call(self):
        HOST, PORT = "localhost", 9764
        server = SocketServer.TCPServer((HOST, PORT), communicator)
        server.serve_forever()
# write this crap with select on socket
    def handle(self):
        # struct which inits: "!6sI" == "IIINIT", unsigned int [Filesize]
        inputRequest, addr = self.request.recvfrom(10)
        init, filesize = struct.unpack("!6sI", inputRequest)
        data = communicator.recvData(addr, filesize)
        # TODO: Encrypt data
        # TODO: Serialize data and pipe it to display or message etc
        
    def recvData(self, addr, filesize):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            port = random.randint(49152, 65535)
            sock.bind("", port)
            sock.connect((addr, port))
            data = sock.recv(filesize)
    
        except Exception as msg:
            print msg
            communicator.createSocket()

        return data