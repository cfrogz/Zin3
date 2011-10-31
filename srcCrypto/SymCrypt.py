#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import bz2
from uuid import uuid4
from json import dumps, loads, dump

class SymCrypt:

    def encryptAES(self, fileID, plaintext, passphrase):
        
        if fileID is None:
            fileID = uuid4()
        
        cipherheader = {'f': str(fileID),
                        's': len(plaintext),
                        'd': plaintext,
                        'p': ""}
        
        while len(str(cipherheader)) % 16 != 0:
            cipherheader['p'] += "."
        passphrase = SHA256.new(passphrase).hexdigest()[:32]
        return AES.new(passphrase, AES.MODE_CBC).encrypt(dumps(cipherheader)).encode("hex")


    def encryptCompressed(self, filename, ciphertext, passphrase, persist):
        try:
            ciphertext = bz2.compress(ciphertext)

        except Exception as msg:
            # just for debugging, this has to be refactored with central logging
            # server ( remember the "help to improve"-project ) !!!
            print msg
            res = input(r"> ")
            print res

        # encode the ciphertext to hex
        ciphertext = ciphertext.encode("hex")

        return self.encryptAES(None, ciphertext, passphrase)
        
    
    def decryptAES(self, inputData=None, passphrase="AAAAAAAAAAAAAAAA", decode=False):
        res = ""
        if decode is True:
            passphrase = SHA256.new(passphrase).hexdigest()[:32]
            res = AES.new(passphrase, AES.MODE_CBC).decrypt(inputData.decode("hex"))
        if decode is False:
            res = AES.new(SHA256.new(passphrase).hexdigest()[:32], AES.MODE_CBC).decrypt(inputData)
        # later loads(res)
        return loads(res)

    def decryptCompressed(self, inputData="", passphrase="AAAAAAAAAAAAAAAA", persist=True):
        # Look for data and serialize decrypted object
        res = self.decryptAES(inputData, passphrase, True)
        # Deflate data
        res['d'] = bz2.decompress(res['d'].decode("hex"))
        
        res['p'] = ""
        # if the persist parameter was set to true (default)
        if persist is True:
            # we want to save the object on harddisk so go on:
            fobj = open("cmnObjectCache/%s" % (res['f']), 'wb')
            dump(res, fobj)
            fobj.flush()
            fobj.close()
        return res