#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import bz2
from uuid import uuid4
from json import dumps, loads, dump

class SymCrypt:

    def appendPadding(self, s, b=16):
		t = b*((len(s)-len(s)%b)/b+1)
		s += '*'
		s = s.ljust(t-1,'0') + '*'
		return s

    def removePadding(self, string):
		string = string[::-1]
		string = string[string.index(chr(42),1)+1::]
		return string[::-1]	

    def encryptAES(self, plaintext, passphrase):
		plaintext = self.appendPadding(plaintext)
		return AES.new( SHA256.new(passphrase).hexdigest()[:32], 
				AES.MODE_CBC, ).encrypt(plaintext)

    def decryptAES(self, ciphertext, passphrase):
		ciphertext = AES.new(SHA256.new(passphrase).hexdigest()[:32],
				AES.MODE_CBC).decrypt(ciphertext)
		return self.removePadding(ciphertext)

    def encryptCompressed(self, filename, ciphertext, passphrase, persist=True):
        ciphertext = bz2.compress(ciphertext)
        ciphertext = ciphertext.encode("hex")
        fileID = str(uuid4())
        padding = ""
        cipherheader = {'f': fileID,
                        's': len(ciphertext),
                        'd': ciphertext
                        }
        return self.encryptAES(dumps(cipherheader), passphrase)
        
    def decryptCompressed(self, input=None, passphrase=None, persist=True):
        res = loads(self.decryptAES(input, passphrase))
        res['d'] = bz2.decompress(res['d'].decode("hex"))
        if persist is True:
            fobj = open("cmnObjectCache/%s" % (res['f']), 'wb')
            dump(res, fobj)
            fobj.flush()
            fobj.close()
        return res