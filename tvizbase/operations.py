# -*- coding: utf-8 -*-

#Permission = authority, 
from .types import *
#from .types import String, ArrayString, Int16, Uint16, Uint64, Amount, Permission, PublicKey, Optional, Bool, ExtensionsComment, Set

# Сериализатор
# https://github.com/VIZ-Blockchain/viz-js-lib/blob/master/src/auth/serializer/src/operations.js

type_op = {
	"create_invite":				[['creator', String], ['balance', Amount], ['invite_key', PublicKey]],
	"claim_invite_balance":			[['initiator', String], ['receiver', String], ['invite_secret', String]],
	
	"award":						[['initiator', String], ['receiver', String], ['energy', Uint16], ['custom_sequence', Uint64], 
									['memo', String], ['beneficiaries', Beneficiaries]],
								
	"transfer":						[['from', String], ['to', String], ['amount', Amount], ['memo', String]],
	"transfer_to_vesting":			[['from', String], ['to', String], ['amount', Amount]],
	"delegate_vesting_shares":		[['delegator', String], ['delegatee', String], ['vesting_shares', Amount]],
	"withdraw_vesting":				[['account', String], ['vesting_shares', Amount]],
	"set_withdraw_vesting_route":	[['from_account', String], ['to_account', String], ['percent', Uint16], ['auto_vest', Bool]],
								
	"account_create":				[['fee', Amount], ['delegation', Amount], ['creator', String], ['new_account_name', String], 
									['master', Permission], ['active', Permission], ['regular', Permission], ['memo_key', PublicKey], 
									['json_metadata', String], ['referrer', String], ['extensions', Set]],
	"account_metadata": 			[['account', String], ['json_metadata', String]],
	"account_witness_proxy":		[['account', String], ['proxy', String]],
	"account_witness_vote":			[['account', String], ['witness', String], ['approve', Bool]],
	"change_recovery_account":		[['account_to_recover', String], ['new_recovery_account', String], ['extensions', Set]],
	"account_update":				[['account', String], ['master', Optional_Permission], ['active', Optional_Permission], 
									['regular', Optional_Permission], ['memo_key', PublicKey], ['json_metadata', String]],
	
	"custom":	 					[['required_active_auths', ArrayString], ['required_regular_auths', ArrayString], 
									['id', String], ['json', String]],
									
	"request_account_recovery ":	[['recovery_account', String], ['account_to_recover', String], ['new_master_authority', Permission], 
									['extensions', Set]],
	"recover_account":				[['account_to_recover', String], ['new_master_authority', Permission], ['recent_master_authority', Permission], 
									['extensions', Set]],
	}
