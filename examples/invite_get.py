# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

secret = '5...'
key = b4.key.get_public(secret)
print(key)


#key = 'VIZ5oDuGMa3DD2YPeDci5ZuuswaMqWh9Zw2qtXPVxABgGNF65hjTv'
tx = b4.get_invite(key)
pprint(tx)


input('next?')


id = 5
tx = b4.get_invite(id)
pprint(tx)


input('end')