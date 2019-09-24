# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

tx = b4.get_invites_list()

for id in tx:
	tx = b4.get_invite(id)
	print(tx["creator"], tx["balance"])

input()