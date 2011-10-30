# a pot contains metainformation about data which
# has to be shared

import socket
import struct
import json
from time import time
from ConfigParser import ConfigParser
from ConfigParser import NoSectionError


try: 
    c = ConfigParser()
    c.read("pot.cfg")
    username = c.get("main", "username")
    key_path = c.get("PGP", "publicKey")

    try:
        key = open(key_path, "r")

    except IOError as msg:
        raise msg
        key = open(key_path, "w")
        key.write("")
        key.close()
        key = open(key_path, "r")

except NoSectionError as msg:
    raise msg


# TODO: Crypt this
try:
    potlist = open('00.tlst.bin', 'r+w')

except IOError as msg:
    raise msg
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
    def createPot(self, potID=None, data=None, firstSharer=None, receivers=[]):
        timestamp = time()
        dataLen = str(len(data))
        receiversLen = str(len(str(receivers)))
        sharerLen = str(len(firstSharer))
        if data <= 0 or data is None: raise MemoryError("Data was not set")
        potStruct = struct.pack("!d" + receiversLen + "s" + sharerLen + "s", timestamp, data, receivers, firstSharer)
        rawPot = {'u': username, 'd': potStruct, 'i': potID}
        json.dump(rawPot, potlist)
        fobj = open(potID, "w")
        
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

    def deletePot(self, potID):
        d_0 = json.load(potlist) # TODO: Check this
        for item in potlist.readlines():
            if item == d_0:
                tmp = str(potlist.read())
                potlist.write(tmp.replace(d_0, ""))
                potlist.flush()

    def downloadPot(self, potID):
        pass

    # receivers are the amount of persons which you share with the main seeder
    # Kai knows Matt, Matt and Kai know Mike: Kai shares data with Matt, If Kai sends
    # the data to Mike, Matt and Kai will serve the data
    def seedPot(self, potID, ):
        pass