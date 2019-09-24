# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

creator = 'ksantoprotein'
wif = '5...'
json_metadata = {"profile": {}}

login = 'reg.ksantoprotein'
password = 'P5...'


#tx = b4.account_create(login, password, creator, wif, fee = 1.0)
#pprint(tx)

tx = b4.account_create(login, password, creator, wif, delegation = True)
pprint(tx)
tx = b4.delegate_vesting_shares(login, 0, creator, wif)
pprint(tx)

input()

