# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

from_account = 'u39.pom'
to_account = 'ksantoprotein'
wif = '5...'

tx = b4.set_withdraw_vesting_route(from_account, to_account, wif)
pprint(tx)
input()