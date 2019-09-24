# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')


to = 'sci-populi'
amount = '0.001'
memo = 'test'

from_account = 'ksantoprotein'
wif = '5...'
tx = b4.transfer(to, amount, from_account, wif, memo = memo)
pprint(tx)

