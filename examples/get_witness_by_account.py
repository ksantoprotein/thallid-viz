# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

account = 'ae'
tx = b4.get_witness_by_account(account)

pprint(tx)
input()