# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

account = 'ksantoprotein'
wif = '5...'	#regular
json_metadata = {"profile": {}, "name": 'Протей'}

tx = b4.get_accounts([account])[0]
print(tx["json_metadata"])

input('ready?')


tx = b4.account_metadata(account, json_metadata, wif)
pprint(tx)

input()

