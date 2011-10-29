# a pot contains metainformation about data which
# has to be shared

import socket
import struct
import json
from time import time

username = "god"
# TODO: Crypt this
torrentlist = open('00.tlst.bin', 'r+w')

class pot(object):
    # receivers: The swarms (circles) which you want
    # to share to.
    # data contains updateID, timestamp, data
    def createPot(self, updateID=None, data=None, firstSharer=None, receivers=[]):
        timestamp = time()
        dataLen = str(len(data))
        receiversLen = str(len(str(receivers)))
        sharerLen = str(len(firstSharer))
        if data <= 0: exit() # TODO: EXCEPTIONHANDLING
        potStruct = struct.pack("!d" + receiversLen + "s" + sharerLen + "s", timestamp, data, receivers, firstSharer)
        rawPot = {'u': username, 'd': potStruct, 'i': updateID}
        json.dump(rawPot, torrentlist)
        
        return rawPot

    def loadPot(self, pot):
        return json.load(torrentlist)

    def deletePot(self, updateID):
        d_0 = json.load(torrentlist) # TODO: Check this
        for item in torrentlist.readlines():
            if item == d_0:
                tmp = str(torrentlist.read())
                torrentlist.write(tmp.replace(d_0, ""))