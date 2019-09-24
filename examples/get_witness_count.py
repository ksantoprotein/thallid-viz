# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')


tx = b4.get_witness_count()

pprint(tx)
input()