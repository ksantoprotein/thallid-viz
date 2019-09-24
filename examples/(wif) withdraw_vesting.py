# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

account = 'u39.pom'
amount = '400.000'
wif = '5...'


tx = b4.withdraw_vesting(account, amount, wif)
pprint(tx)
input()