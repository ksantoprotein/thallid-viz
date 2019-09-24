# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')


initiator = 'ksantoprotein'
receiver = 'ksantoprotein'
invite_secret = '5...'
wif = '5...'

tx = b4.claim_invite_balance(initiator, receiver, invite_secret, wif)
pprint(tx)
input()



