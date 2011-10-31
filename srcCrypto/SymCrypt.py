#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	@todo: check'n'merge
"""
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

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

