# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')


account = 'ksantoprotein'
wif = '5...'

witnesses = ['solox', 'lex', 'lexai']
approve = True

for witness in witnesses:
	tx = b4.get_accounts([account])[0]
	print(tx["name"], 'witness:', tx["witness_votes"], 'proxy:', tx["proxy"])

	input('ready?')

	tx = b4.account_witness_vote(account, witness, wif, approve = approve)
	pprint(tx)

input()

