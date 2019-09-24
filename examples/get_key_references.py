# -*- coding: utf-8 -*-

import json
from pprint import pprint

from tvizbase.api import Api


print('connect')
b4 = Api()
print('try call')

public_key = 'VIZ7tnDdbUmjT89YQsokHagcjwzVN1FPWL86wUe6S3TNUgJaYvn2i'

tx = b4.get_key_references(public_key)

print(tx)
input()