# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

id = 'viz_contract'
payload = {"app": 'thallid', "spell": 'fireball', "damage": 100}

account = 'ksantoprotein'
wif = '5...'


tx = b4.custom(id, payload, account, wif)
pprint(tx)
input()