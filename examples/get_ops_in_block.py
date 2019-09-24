# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

block = 3058791

tx = b4.get_ops_in_block(block)

pprint(tx)
input()