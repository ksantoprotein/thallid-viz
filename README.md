# thallid-viz - Python Library for VIZ

Thallid-VIZ библиотека для блокчейна VIZ


# Installation

https://github.com/ksantoprotein/thallid-viz.git

# Documentation


# Usage examples

#### Award
``` python
from tvizbase.api import Api

b4 = Api()

initiator = 'ksantoprotein'
receiver = 'ksantoprotein'
energy = 0
wif = '5...'

memo = 'test'

b4.award(initiator, receiver, energy, wif, memo = memo)
```


#### Transfer
``` python
from tvizbase.api import Api

b4 = Api()

to = 'sci-populi'
amount = '0.001'
memo = 'test'

from_account = 'ksantoprotein'
wif = '5...'
b4.transfer(to, amount, from_account, wif, memo = memo)

```

#### Get_Dynamic_Global_Properties
``` python
from tvizbase.api import Api
from pprint import pprint

b4 = Api()

tx = b4.get_dynamic_global_properties()
pprint(tx)

```

#### Get_Accounts
``` python
from tvizbase.api import Api
from pprint import pprint

b4 = Api()

accounts = ['ksantoprotein', 'sci-populi']
tx = b4.get_accounts(accounts)
for account in tx:
	pprint(account)
	input('next')

```
