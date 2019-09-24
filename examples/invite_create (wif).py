# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')


creator = 'ksantoprotein'
wif = '5...'
balance = 1.100

psw = 'P5...'
keys = b4.key.get_keys(creator, psw)
invite_key = keys["public"]["active"]


tx = b4.create_invite(creator, balance, invite_key, wif)
pprint(tx)

if tx:
	with open('invite_create.csv', 'a', encoding = 'utf8') as f:
		f.write(keys["private"]["active"] + ' ' + str(balance) + '\n')

input()

