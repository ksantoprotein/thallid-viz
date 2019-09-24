# -*- coding: utf-8 -*-

from pprint import pprint
import json

import hashlib
from binascii import hexlify, unhexlify
from graphenebase.account import PrivateKey
from .storage import prefix

	
class Key():

	def __init__(self):
		self.roles = ["posting", "regular", "active", "memo", "owner", "master"]	# posting=>regular, owner=>master
		self.prefix = prefix
		

	def get_keys(self, account, password):

		keys = {"login": account, "password": password, "private": {}, "public": {}}
		
		for role in self.roles:

			b = bytes(account + role + password, 'utf8')
			s = hashlib.sha256(b).digest()
			k = hexlify(s).decode('ascii')
			#b58 = Base58(k)
			#wif = format(b58, "WIF")
			#print(role, wif)
			pk = PrivateKey(wif = k, prefix = self.prefix)
			keys["private"][role] = str(pk)
			keys["public"][role] = str(pk.pubkey)
			
		return(keys)
		
		
	def get_public(self, wif):
		pk = PrivateKey(wif, prefix = self.prefix)
		return(str(pk.pubkey))
		
		
	def is_key(self, wif, gls):
		pk = PrivateKey(wif, prefix = self.prefix)
		if str(pk.pubkey) == gls:
			return True
		return False


if __name__ == '__main__':

	pass
