# a pot contains metainformation about data which
# has to be shared

import socket
import struct
import json
from time import time
from ConfigParser import ConfigParser

try:
    c = ConfigParser()
    c.read("pot.cfg")
    username = c.get("main", "username")
except Exception:
    print Exception

# TODO: Crypt this
try:
    potlist = open('00.tlst.bin', 'r+w')

except IOError as msg:
    print msg
    potlist = open('00.tlst.bin', 'w')
    potlist.write("")
    potlist.flush()
    potlist.close()
    potlist = open('00.tlst.bin', 'r+w')
    print "Created file."

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
        json.dump(rawPot, potlist)
        fobj = open(updateID, "w")
        
        potlist.flush()
        
        return rawPot

    def loadPot(self, pot):
        return json.load(potlist)
    
    def changePot(self, pot={}, newPot={}):
        oldPot = json.load(potlist)
        for item in potlist.readlines():
            if item == oldPot:
                tmp = str(potlist.read())
                if newPot is {}:
                    raise "ERROR NEW POT IS EMPTY"
                    break
                else:
                    potlist.write(tmp.replace(oldPot, newPot))
                potlist.flush()

    def deletePot(self, updateID):
        d_0 = json.load(potlist) # TODO: Check this
        for item in potlist.readlines():
            if item == d_0:
                tmp = str(potlist.read())
                potlist.write(tmp.replace(d_0, ""))
                potlist.flush()