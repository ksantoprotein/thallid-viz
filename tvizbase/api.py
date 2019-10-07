# -*- coding: utf-8 -*-

from pprint import pprint
import json
import math

from .ws_client import WsClient
from .broadcast import Tx
from .key import Key
from .storage import time_format, asset_precision, rus_d, rus_list, prefix, fee, fee_asset, fee_delegation, fee_asset_delegation

from datetime import datetime, timedelta

from time import sleep, time

from random import randint



class Api():

	def __init__(self, **kwargs):

		# Пользуемся своими нодами или новыми
		nodes = kwargs.pop("nodes", None)
		if nodes:
			self.rpc = WsClient(nodes = nodes)
		else:
			self.rpc = WsClient()

		config_viz = self.rpc.call('get_config')
		self.CHAIN_BANDWIDTH_PRECISION = int(config_viz["CHAIN_BANDWIDTH_PRECISION"])
		self.BANDWIDTH_RESERVE_PERCENT = int(config_viz["CONSENSUS_BANDWIDTH_RESERVE_PERCENT"])
		self.BANDWIDTH_RESERVE_BELOW = int(config_viz["CONSENSUS_BANDWIDTH_RESERVE_BELOW"])
		
		self.asset_precision = asset_precision
		self.fee = fee
		self.fee_asset = fee_asset
		self.fee_delegation = fee_delegation
		self.fee_asset_delegation = fee_asset_delegation
		
		self.broadcast = Tx(self.rpc)
		self.finalizeOp = self.broadcast.finalizeOp
		
		self.key = Key()
		
		self.rus_d = rus_d
		
		
######### API ##########

######### account_by_key #########

	def get_key_references(self, public_key):
			
		'''
		Позволяет узнать какому логину соответсвует публичный ключ
		#public_key = 'GLS6RGi692mJSNkdcVRunY3tGieJdTsa7AZeBVjB6jjqYg98ov5NL'
		Но не позволяет если есть авторити у аккаунта
		'''
		
		res = self.rpc.call('get_key_references', [public_key])
		if not res:
			return([])
		return(res[0])		# list
		
######### account_history #########		
		
	def get_account_history(self, account, **kwargs):
	
		start_limit = kwargs.pop("start_limit", 1000)			#лимит одновременного запроса
		op_limit = kwargs.pop("type_op", 'all')					#какие операции сохранять, list
		age_max = kwargs.pop("age", 7*24*60*60)					#время в сек до какой операции сканировать

		info = self.get_dynamic_global_properties()
		if not info:
			print('error in global data')
			return False
		raw = []
					
		start_block, flag, n = 999999999, True, 0
		while flag:
			history = self.rpc.call('get_account_history', account, start_block, start_limit)

			for h in reversed(history):
				number = h[0]
				block = h[1]["block"]
				timestamp = h[1]["timestamp"]
				type_op = h[1]["op"][0]

				op = h[1]["op"][1]
				op["number"] = number
				op["block"] = block
				op["timestamp"] = timestamp
				op["type_op"] = type_op
				
				if type_op in op_limit or op_limit == 'all':
				
					raw.append(op)
					#pprint(op)
					#input('next')
				
				last_history_time = datetime.strptime(timestamp, time_format)
				age = (info["now"] - last_history_time).total_seconds() / 1
				if age > age_max:
					flag = False
					break
				
			start_block = h[0] - 1
			if start_block < start_limit:
				start_limit = start_block
			if start_limit <= 0:
				flag = False
			n += 1
			print(start_block, 'scan', n * start_limit)
	
		return(raw)
			
######### committee_api #########

######### database_api #########

	def get_account_count(self):
		# Возвращает количество зарегестрированных пользователей
		return(int( self.rpc.call('get_account_count') ))
	
		
	def get_accounts(self, logins, **kwargs):							#need correct
	
		'''
		Перерасчитываются некоторые параметры по аккаунту
		"VIZ", "SHARES" - ликвидные токены
		"bandwidth" = {	"avail" - всего доступно в кБ
						"used" - использовано в кБ
						"free" - доступно в кБ}
		'''
		
		add_follow = kwargs.pop("follow", False)	###

		accounts = self.rpc.call('get_accounts', logins)
		info = self.get_dynamic_global_properties()
		if not info:
			print('error in global data')
			return False
		
		for account in accounts:

			try:
				# Определение SHARES
				vesting_shares = float(str(account["vesting_shares"]).split()[0])
				delegated = float(str(account["delegated_vesting_shares"]).split()[0])
				received = float(str(account["received_vesting_shares"]).split()[0])
				#account["SHARES"] = round( (vesting_shares + received - delegated) * info["viz_per_vests"], asset_precision["SHARES"])
				account["SHARES"] = round( (vesting_shares + received - delegated), asset_precision["SHARES"])
			except:
				return False

			# Определение ликвидных токенов
			
			account["VIZ"] = float(str(account["balance"]).split()[0])

			# Определение реальной энергии 1-10000
			VP = float(account["energy"])
			last_vote_time = datetime.strptime(account["last_vote_time"], time_format)
			age = (info["now"] - last_vote_time).total_seconds() / 1
			actualVP = VP + (10000 * age / 432000)

			#print(actualVP)
			if actualVP > 10000:
				account["power"] = 10000
			else:
				account["power"] = round(actualVP)
			
			# Определение rshares
			'''
			vesting_shares = int(1e6 * account["golos_power"] / info["viz_per_vests"])
			
			max_vote_denom = info["vote_regeneration_per_day"] * (5 * 60 * 60 * 24) / (60 * 60 * 24)
			used_power = int((account["voting_power"] + max_vote_denom - 1) / max_vote_denom)
			rshares = ((vesting_shares * used_power) / 10000)
			account["rshares"] = round(rshares)
			account["add_reputation"] = round(rshares / 64)
			'''
			
			# Определение стоимости апвота
			account["TVALUE"] = round(100 * 10000 * account["SHARES"] * info["total_reward_fund"] / info["total_reward_shares"], asset_precision["SHARES"])
			account["VALUE"] = round(100 * account["power"] * account["SHARES"] * info["total_reward_fund"] / info["total_reward_shares"], asset_precision["SHARES"])
			account["RVALUE"] = round(account["power"] * account["SHARES"] * info["total_reward_fund"] / info["total_reward_shares"], asset_precision["SHARES"])
			#info["viz_per_vests"]
			'''
			value_golos = round(account["rshares"] * info["total_reward_fund"] / info["total_reward_shares"], asset_precision["GOLOS"])
			value_gbg = round(value_golos * median_price, asset_precision["GBG"])
			order_gbg = round(value_golos * order_price, asset_precision["GBG"])
			account["value"] = {"GOLOS": value_golos, "GBG": value_gbg}
			account["order"] = {"GOLOS": value_golos, "GBG": order_gbg}
			'''
					
			# Определение update_account_bandwidth
			# BANDWIDTH_RESERVE_PERCENT
			# BANDWIDTH_RESERVE_BELOW: 500000000,
			average_bandwidth = int(account["average_bandwidth"])
			max_virtual_bandwidth = int(info["max_virtual_bandwidth"]) / self.CHAIN_BANDWIDTH_PRECISION
			average_seconds = 7 * 24 * 60 * 60
			last_time = datetime.strptime(account["last_bandwidth_update"], time_format)
			age_after = int((info["now"] - last_time).total_seconds() / 1)			# seconds
			
			if age_after >= average_seconds:
				new_account_average_bandwidth = 0
			else:
				new_account_average_bandwidth = (((average_seconds - age_after) * average_bandwidth) / average_seconds)
			
			if account["SHARES"] < self.BANDWIDTH_RESERVE_BELOW / self.CHAIN_BANDWIDTH_PRECISION:		# 500 SHARES
				#account_vshares = info["total_vesting_shares"] * (self.BANDWIDTH_RESERVE_PERCENT / 10000) / info["bandwidth_reserve_candidates"]		# 10%
				k = (self.BANDWIDTH_RESERVE_PERCENT / 10000) / info["bandwidth_reserve_candidates"]		# 10%
			else:
				#account_vshares = account["SHARES"] * (1 - (self.BANDWIDTH_RESERVE_PERCENT / 10000))		# -10%
				k = (account["SHARES"] / info["total_vesting_shares"]) * (1 - (self.BANDWIDTH_RESERVE_PERCENT / 10000))		# -10%
				
			avail = k * max_virtual_bandwidth
				
			#avail = (account_vshares / info["total_vesting_shares"]) * max_virtual_bandwidth / self.CHAIN_BANDWIDTH_PRECISION
				
			used = new_account_average_bandwidth / self.CHAIN_BANDWIDTH_PRECISION
			
			used_kb = round(used / 1024, 3)
			avail_kb = round(avail / 1024, 3)
			
			max_virtual_bandwidth_kb = round(max_virtual_bandwidth / (1024), 3)
			#print(max_virtual_bandwidth_kb, 'kB max_virtual_bandwidth')
			
			account["bandwidth"] = {
							"avail": avail_kb,
							"used": used_kb,
							"free": round(avail_kb - used_kb, 3),
							}


		return(accounts)
		

	def get_block(self, n):
		return self.rpc.call('get_block', str(n))
		

	def get_chain_properties(self):
		return self.rpc.call('get_chain_properties')


	def get_config(self):
		return self.rpc.call('get_config')
		

	def get_database_info(self):
		return self.rpc.call('get_database_info')


	def get_dynamic_global_properties(self):						#need correct

		# Returns the global properties
		prop = self.rpc.call('get_dynamic_global_properties')

		# Obtain STEEM/VESTS ratio
		for p in ["total_vesting_fund", "total_reward_fund", "total_vesting_shares"]:
			value = prop.pop(p, None)
			if not value:
				return False
			prop[p] = float(value.split()[0])
			
		for p in ["total_reward_shares", "last_irreversible_block_num", "vote_regeneration_per_day", 
				"bandwidth_reserve_candidates", "max_virtual_bandwidth"]:
			value = prop.pop(p, None)
			if not value:
				return False
			prop[p] = int(value)
			
		prop["viz_per_vests"] = prop["total_vesting_fund"] / prop["total_vesting_shares"]
		prop["now"] = datetime.strptime(prop["time"], time_format)

		return(prop)

		
	#def get_next_scheduled_hardfork(self):
	#	return self.rpc.call('get_next_scheduled_hardfork')

		
	#def get_hardfork_version(self):
	#	return self.rpc.call('get_hardfork_version')
		
		
	def get_potential_signatures(self, tx):									#OK возвращает список логинов
		return self.rpc.call('get_potential_signatures', tx)
		

	#def get_recovery_request(self, tx, keys):								#Bad
	#	return self.rpc.call('get_recovery_request', tx, keys)

	
	def get_all_accounts(self):
	
		n = self.get_account_count()
		limit = 1000
		print('find', n, 'accounts')
		
		accounts_dict = {}
		start_login = 'a'
		while True:
			print(start_login)
			logins = self.rpc.call('lookup_accounts', start_login, limit)
			
			if len(logins) == 1 and logins[0] == start_login:
				accounts = self.get_accounts(logins)
				for account in accounts:
					accounts_dict[account["name"]] = account
				break

			accounts = self.get_accounts(logins[:-1])
			for account in accounts:
				accounts_dict[account["name"]] = account

			start_login = logins[-1:][0]
	
		return accounts_dict
		
######### operation_history #########
	
	def get_ops_in_block(self, n):
		block = self.rpc.call('get_ops_in_block', str(n), True)
		return block

######### invite #########

	def claim_invite_balance(self, initiator, receiver, invite_secret, wif, **kwargs):
	
		ops = []
		t = {
			"initiator": initiator,
			"receiver": receiver,
			"invite_secret": invite_secret,
			}
		ops.append(['claim_invite_balance', t])
		tx = self.finalizeOp(ops, wif)
		return tx


	def create_invite(self, creator, balance, invite_key, wif, **kwargs):
	
		#asset = 'VIZ'	###
		asset = self.fee_asset

		ops = []
		t = {
			"creator": creator,
			"balance": '{:.{precision}f} {asset}'.format(
						float(balance),
						precision = self.asset_precision[asset],
						asset = asset
						),
			"invite_key": invite_key,
			}
		ops.append(['create_invite', t])
		tx = self.finalizeOp(ops, wif)
		return tx

		
	def get_invites_list(self):														#maybe correct
		return(self.rpc.call('get_invites_list', '0'))

		
	def get_invite(self, wtf):
	
		'''
		{
		"id": 6,
		"creator": "ae",
		"receiver": "",
		"invite_key": "VIZ5oDuGMa3DD2YPeDci5ZuuswaMqWh9Zw2qtXPVxABgGNF65hjTv",
		"invite_secret": "",
		"balance": "1.000 VIZ",
		"claimed_balance": "0.000 VIZ",
		"create_time": "2018-10-10T18:31:12",
		"claim_time": "1970-01-01T00:00:00",
		"status": 0
		}	
		'''
		
		try:
			# Проверям id ли это
			id = int(wtf)
			op = self.rpc.call('get_invite_by_id', str(id))
		except:
			# Проверям wif ли это
			op = self.rpc.call('get_invite_by_key', wtf) if wtf[:3] == 'VIZ' else None
		if not op:
			return False

		for cmd in ['balance', 'claimed_balance']:
			op[cmd] = float(op[cmd].split()[0])
			
		op["active"] = True if int(op["status"]) == 0 else False
		
		return op
		
######### witness_api #########
		
	def get_active_witnesses(self):
		return self.rpc.call('get_active_witnesses')
		
	def get_witness_count(self):
		return self.rpc.call('get_witness_count')
		
	def get_witness_schedule(self):
		return self.rpc.call('get_witness_schedule')
		
	def get_witness_by_account(self, account):
		return self.rpc.call('get_witness_by_account', account)
		
	#def get_witnesses(self, ids):
	#	return self.rpc.call('get_witnesses', ids)
	
	#def get_witnesses_by_vote(self, start, limit):
	#	return self.rpc.call('get_witnesses_by_vote', start, limit)
	
	def lookup_witness_accounts(self, start, limit):
		return self.rpc.call('lookup_witness_accounts', start, limit)
	
		
		

######### differ #########
		
	def is_login(self, login):

		#Проверка существования логина
		account = self.get_accounts([login])
		if account:
			public_key = account[0]["memo_key"]
			return(public_key)
			
		return False

		
	def check_login(self, login):

		if len(login) > 25:	## скорректировать под параметр блокчейна в инициализации
			return False
		if login[0] not in list('abcdefghijklmnopqrstuvwxyz'):
			return False
		for l in list(login[1:]):
			if l not in list('abcdefghijklmnopqrstuvwxyz0123456789.-'):
				return False
			
		return True

########## BROADCAST #########

	def award(self, initiator, receiver, energy, wif, **kwargs):

		#asset = 'VIZ'
		asset = self.fee_asset
		
		custom_sequence = kwargs.pop('custom_sequence', 0)
		memo = kwargs.pop('memo', '')

		ops = []
		op = {
			"initiator": initiator,
			"receiver": receiver,
			"energy": int(energy),
			"custom_sequence": custom_sequence,
			"memo": memo,
			"beneficiaries": [],
			#"beneficiaries": [{"account": 'ksantoprotein', "weight": 1000}],
			}
		ops.append(['award', op])
		tx = self.finalizeOp(ops, wif)
		return tx
	

	def award10(self, initiator, receiver, energy, wif, **kwargs):

		#asset = 'VIZ'
		asset = self.fee_asset
		
		custom_sequence = kwargs.pop('custom_sequence', 0)
		memo = kwargs.pop('memo', '')

		ops = []
		op = {
			"initiator": initiator,
			"receiver": receiver,
			"energy": int(energy),
			"custom_sequence": custom_sequence,
			"memo": memo,
			#"beneficiaries": [],
			"beneficiaries": [{"account": 'ksantoprotein', "weight": 1000}],	#list {}
			}
		ops.append(['award', op])
		tx = self.finalizeOp(ops, wif)
		return tx

		
	def transfer(self, to, amount, from_account, wif, **kwargs):

		#asset = 'VIZ'
		asset = self.fee_asset
		memo = kwargs.pop('memo', '')

		ops = []
		op = {
			"from": from_account,
			"to": to,
			"amount": '{:.{precision}f} {asset}'.format(
						float(amount),
						precision = self.asset_precision[asset],
						asset = asset
						),
			"memo": memo
			}
		ops.append(['transfer', op])
		tx = self.finalizeOp(ops, wif)
		return tx
		
		
	def transfers(self, raw_ops, from_account, wif):

		#asset = 'VIZ'
		asset = self.fee_asset
		# to, amount, asset, memo

		ops = []
		for raw in raw_ops:
			to, amount, memo = raw
			op = {
				"from": from_account,
				"to": to,
				"amount": '{:.{precision}f} {asset}'.format(
							float(amount),
							precision = self.asset_precision[asset],
							asset = asset
							),
				"memo": memo
				}
			ops.append(['transfer', op])
		
		tx = self.finalizeOp(ops, wif)
		return tx

		
	def transfer_to_vesting(self, to, amount, from_account, wif, **kwargs):

		# to, amount, from_account
		#asset = 'VIZ'
		asset = self.fee_asset

		ops = []
		op = {
			"from": from_account,
			"to": to,
			"amount": '{:.{precision}f} {asset}'.format(
						float(amount),
						precision = self.asset_precision[asset],
						asset = asset
						),
			}
		ops.append(['transfer_to_vesting', op])
		tx = self.finalizeOp(ops, wif)
		return tx


	def delegate_vesting_shares(self, to, amount, from_account, wif, **kwargs):

		# to, amount, from_account
		#asset = 'SHARES'
		asset = self.fee_asset_delegation

		ops = []
		op = {
			"delegator": from_account,
			"delegatee": to,
			"vesting_shares": '{:.{precision}f} {asset}'.format(
						float(amount),
						precision = self.asset_precision[asset],
						asset = asset
						),
			}
		ops.append(['delegate_vesting_shares', op])
		tx = self.finalizeOp(ops, wif)
		return tx
		

	def withdraw_vesting(self, account, amount, wif, **kwargs):

		asset = 'SHARES'

		ops = []
		op = {
			"account": account,
			"vesting_shares": '{:.{precision}f} {asset}'.format(
						float(amount),
						precision = self.asset_precision[asset],
						asset = asset
						),
			}
		ops.append(['withdraw_vesting', op])
		tx = self.finalizeOp(ops, wif)
		return tx
		
		
	def set_withdraw_vesting_route(self, from_account, to_account, wif, **kwargs):

		percent = kwargs.get("percent", 10000)
		auto_vest = kwargs.get("auto_vest", False)
		ops = []
		op = {
			"from_account": from_account,
			"to_account": to_account,
			"percent": percent,
			"auto_vest": auto_vest,
			}
		ops.append(['set_withdraw_vesting_route', op])
		tx = self.finalizeOp(ops, wif)
		return tx

		
	def account_create(self, login, password, creator, wif, delegation = False, **kwargs):

		# login = account name must be at most 25 chars long, check if account already exists
		# roles = ["regular", "active", "memo", "master"]
		paroles = self.key.get_keys(login, password)

		fee = kwargs.pop("fee", self.fee)
		
		fees = [0.0, self.fee_delegation] if delegation else [fee, 0.0]
		fee, fee_delegation = fees
		
		json_metadata = kwargs.pop("json_metadata", {"profile": {}})	###
			
		owner_key_authority = [ [paroles["public"]["master"], 1] ]
		active_key_authority = [ [paroles["public"]["active"], 1] ]
		posting_key_authority = [ [paroles["public"]["regular"], 1] ]
		memo = paroles["public"]["memo"]
		
		owner_accounts_authority = []
		#active_accounts_authority = [ [creator, 1] ]
		#posting_accounts_authority = [ [creator, 1] ]
		active_accounts_authority = []
		posting_accounts_authority = []
		
		#asset = 'VIZ'
		asset = self.fee_asset
		asset_delegation = self.fee_asset_delegation
		
		ops = []
		op = {
			#"fee": '1.000 VIZ',
			#"delegation": '0.000000 SHARES',
			"fee": '{:.{precision}f} {asset}'.format(
						float(fee),
						precision = self.asset_precision[asset],
						asset = asset
						),
			"delegation": '{:.{precision}f} {asset}'.format(
						float(fee_delegation),
						precision = self.asset_precision[asset_delegation],
						asset = asset_delegation
						),
			"creator": creator,
			"new_account_name": login,
			"master": {
				'weight_threshold': 1,
				'account_auths': owner_accounts_authority,
				'key_auths': owner_key_authority,
			},
			"active": {
				'weight_threshold': 1,
				'account_auths': active_accounts_authority,
				'key_auths': active_key_authority,
			},
			"regular": {
				'weight_threshold': 1,
				'account_auths': posting_accounts_authority,
				'key_auths': posting_key_authority,
			},
			"memo_key": memo,
			"json_metadata": json.dumps(json_metadata, ensure_ascii = False),
			"referrer": '',
			"extensions": [],
		}
		ops.append(['account_create', op])
		tx = self.finalizeOp(ops, wif)
		return tx
		

	def account_metadata(self, account, json_metadata, wif):
	
		ops = []
		op = {
			"account": account,
			"json_metadata": json.dumps(json_metadata, ensure_ascii = False)
			}
		ops.append(['account_metadata', op])

		tx = self.finalizeOp(ops, wif)
		return tx
		

	def account_witness_proxy(self, account, proxy, wif):
	
		ops = []
		op = {
			"account": account,
			"proxy": proxy,
			}
		ops.append(['account_witness_proxy', op])

		tx = self.finalizeOp(ops, wif)
		return tx
		

	def account_witness_vote(self, account, witness, wif, **kwargs):
	
		ops = []
		op = {
			"account": account,
			"witness": witness,
			"approve": kwargs.get("approve", True),		#True - vote, False - del vote
			}
		ops.append(['account_witness_vote', op])

		tx = self.finalizeOp(ops, wif)
		return tx
		
		
	def change_recovery_account(self, account, recovery_account, wif):
	
		ops = []
		op = {
			"account_to_recover": account,
			"new_recovery_account": recovery_account,
			"extensions": [],
			}
		ops.append(['change_recovery_account', op])

		tx = self.finalizeOp(ops, wif)
		return tx
		

	def custom(self, id, payload, account, wif, **kwargs):
	
		ops = []
		op = {
			"required_active_auths": [],
			"required_regular_auths": [account],
			"id": id,
			"json": json.dumps(payload, ensure_ascii = False)
			}
		ops.append(['custom', op])

		tx = self.finalizeOp(ops, wif)
		return tx
		
		
	def account_update_password(self, account, password, wif):

		paroles = self.key.get_keys(account, password)
		
		
		tx = self.get_accounts([account])[0]		
		json_metadata = tx.get("json_metadata", {"profile": {}})	###
		
		print(json_metadata)
		pprint(tx["master_authority"])
		pprint(tx["active_authority"])
		pprint(tx["regular_authority"])
		print(tx["memo_key"])
		
		#public = self.key.get_public(wif)
		#print(public, tx["master_authority"]["key_auths"])
		
		input('ready?')
		
		owner_key_authority = [ [paroles["public"]["master"], 1] ]
		active_key_authority = [ [paroles["public"]["active"], 1] ]
		posting_key_authority = [ [paroles["public"]["regular"], 1] ]
		#owner_key_authority = False
		#active_key_authority = False
		#posting_key_authority = False
		
		memo = paroles["public"]["memo"]
		
		# Очистка авторити
		owner_accounts_authority = []
		active_accounts_authority = []
		posting_accounts_authority = []
		
		ops = []
		op = {
			"account": account,
			"master": {
						'weight_threshold': 1,
						'account_auths': owner_accounts_authority,
						'key_auths': owner_key_authority,
						},
			"active": {
						'weight_threshold': 1,
						'account_auths': active_accounts_authority,
						'key_auths': active_key_authority,
						},
			"regular": {
						'weight_threshold': 1,
						'account_auths': posting_accounts_authority,
						'key_auths': posting_key_authority,
						},
			"memo_key": memo,
			#"json_metadata": json.dumps(json_metadata, ensure_ascii = False),
			"json_metadata": json_metadata,
			}
		ops.append(['account_update', op])
		
		tx = self.finalizeOp(ops, wif)
		return tx
				
