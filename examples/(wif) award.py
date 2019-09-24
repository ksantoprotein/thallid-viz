# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

initiator = 'ksantoprotein'
receiver = 'ksantoprotein'
energy = 0
wif = '5...'

memo = 'test'

tx = b4.award(initiator, receiver, energy, wif, memo = memo)
pprint(tx)
input()