# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

accounts = {
			"sci-populi": '5...',
			"azino777": '5...',
			"azino37ace": '5...',
			}


proxy = 'ksantoprotein'

for account, wif in accounts.items():

	tx = b4.get_accounts([account])[0]
	print(tx["name"], tx["proxy"], tx["SHARES"], 'SHARES')
	
	if tx["proxy"] != proxy:

		input('ready?')

		tx = b4.account_witness_proxy(account, proxy, wif)
		pprint(tx)

input()

