from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import bz2
import json
from time import time
from struct import pack

class crypto(object):
    def encrypt(self, userID=None, input=None, key="AAAAAAAAAAAAAAAA"):
        fobj = open("cmn/%s" % (SHA256.new(str(userID)+(str(input))).hexdigest()), "w")
        text = str(input).encode("hex")


        print "compressing."
        compressed = bz2.compress(text)
        header = {'u': userID,'d': str(compressed).encode("hex"), 'l': len(compressed.encode("hex")), 'p': ''}
        print len(compressed)

        print len(str(header))
        while len(str(header)) % 16 != 0:
            header['p'] += "A"
        print len(str(header))
        print header
        t1 = time()

        print "Starting ciphering, this could take a while.."
        r = AES.new(SHA256.new(key).hexdigest()[:32])
        res = ""
        if len(str(header)) % 16 == 0:
            res = r.encrypt(str(header)).encode("hex")
        else:
            print "WTF"
        t2 = time()
        print res
        print "Finished encrypting, took %s seconds" % (t2-t1)

        json.dump(res, fobj)
        fobj.close()
        return res
    
    
    # TODO: Debug this (FIXME: Error while deflating)
    def decrypt(self, name, key):
        fobj = open("cmn/%s" % (name), "r")
        obj = fobj.read()
        print obj
        print type(obj)
        print "\n" + obj
        print "Decrypting.."
        r = AES.new(SHA256.new(key).hexdigest()[:32])
        print len(obj)
        res = r.decrypt(obj)
        print str(res.decode("hex")).decode("hex")
        test = json.loads(res.decode("hex"))
        print type(test)
        print test
        fobj.close()
        print res
        return res