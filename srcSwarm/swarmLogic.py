# This class contains the logic of the friendlist (here: swarms)
# and the datacommunication (only possible with friends)

import socket
import select
import pot

class swarm(object):
    def __init__(self):
        self.p = pot.pot()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # we need a socket where we pipe the data through (select on this socket)

#TODO: CRYPTO
    # receiver has to contain a list with receiver IDs
    # the IDs have to be looked up to their IPs
    def sharePot(self, receivers, potID):
        pot = self.p.loadPot(potID)
        for receiver in receivers:
            self.s.sendto(str(pot), (receiver, 4223))
        return 0

    # Wait for some input pot, add it to downloadlist and start receiving
    def beggingForPot(self, sock):
        sock.listen(5)
        sock.bind(("", 4223))
        
        sockets = select.select([sock], [], [])
        for s in sockets[0]:
            data, addr = s.recvfrom(1024) # TODO: This has to be calculated by an init packet
            # TODO: End work here..

class swarmCommunication(object):
    pass