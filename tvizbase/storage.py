# -*- coding: utf-8 -*-

chain_id = '2040effda178d4fffff5eab7a915d4019879f5205cc5392e4bcced2b6edda0cd'		# VIZ
prefix = 'VIZ'
fee = '1.000'
fee_asset = 'VIZ'
fee_delegation = '10.000000'
fee_asset_delegation = 'SHARES'
time_format = '%Y-%m-%dT%H:%M:%S'
time_format_utc = '%Y-%m-%dT%H:%M:%S%Z'
expiration = 60


nodes = [
		#'wss://viz.lexa.host/ws'		### https://viz.lexa.host/	seed.viz.lexa.host:2001
		
		
		#'wss://solox.world/ws',			### https://solox.world/
		
		'https://node.viz.cx',
		'https://vizrpc.lexa.host',
		'https://viz.lexai.host',
		
		'https://solox.world/',
		'https://viz-node.dpos.space/',
		'https://node.viz.plus/'
		
		#https://testnet.lexai.host
		
		#'https://solox.world/',		# old
		
		#'wss://ws.viz.ropox.app',
		
		#'ws://37.192.123.64:9093',	# not full
		
		#'wss://viz.lexai.host',	# old
		#'https://viz.lexa.host/',
		#'wss://viz.lexa.host/ws',
		#'seed.viz.lexa.host:2001',
		#'wss://lexai.host/ws',		
		
		#'wss://testnet.viz.world',
		#'ws://api.viz.blckchnd.com/ws',
		#'wss://api.viz.blckchnd.com/ws',
		]

# https://github.com/VIZ-World/viz-world-js/blob/master/src/api/methods.js
api_list = {
			"account_by_key": ['get_key_references'],				# ok
			"account_history": ['get_account_history'],				# ok "params": ["account", "from", "limit"]
			"committee_api": [
							'get_committee_request',				#
							'get_committee_request_votes',			#
							'get_committee_requests_list',			#
							],
			"database_api": [
							'get_account_count',					# ok
							'get_accounts',							# ok
							'get_accounts_on_sale',
							'get_block',							# ok
							'get_block_header',						#
							'get_chain_properties',					# ok
							'get_config',							# ok
							'get_database_info',					# ok
							'get_dynamic_global_properties',		# ok
							'get_escrow',							#
							'get_expiring_vesting_delegations',		#
							'get_hardfork_version',					#
							'get_next_scheduled_hardfork',			#
							'get_owner_history',					# not "params": ["account"] изменение право собственности
							'get_potential_signatures',				# ok
							'get_proposed_transaction',				# ???
							'get_recovery_request',					# not
							'get_required_signatures',				# ???
							'get_transaction_hex',					# "params": ["trx"]
							'get_vesting_delegations',				#
							'get_withdraw_routes',					#
							'lookup_account_names',					#
							'lookup_accounts',						# ok in get_all_accounts
							'verify_account_authority',				#
							'verify_authority'						#
							],
			"follow": [
							'get_blog',								#
							'get_blog_authors',						#
							'get_blog_entries',						#
							'get_feed',								#
							'get_feed_entries',						#
							'get_follow_count',						#
							'get_followers',						#
							'get_following',						#
							'get_reblogged_by'						#
						],
			"invite_api": [
							'get_invites_list',						# ok
							'get_invite_by_id',						# ok
							'get_invite_by_key',					# ok
							],
			"network_broadcast_api": [
							'broadcast_block',						#
							'broadcast_transaction',				#
							'broadcast_transaction_synchronous',	#
							'broadcast_transaction_with_callback'	#
							],
			"operation_history": [
							'get_ops_in_block',						# ok
							'get_transaction'						#
							],
			"social_network": [
							'get_account_votes',					#
							'get_active_votes',						#
							'get_all_content_replies',				#
							'get_committee_request',
							'get_committee_request_votes',
							'get_committee_requests_list',								
							'get_content',							#
							'get_content_replies',					#
							'get_replies_by_last_update'			#
							],
			"tags": [
							'get_discussions_by_active',			#
							'get_discussions_by_author_before_date',#
							'get_discussions_by_blog',				#
							'get_discussions_by_cashout',			#
							'get_discussions_by_children',			#
							'get_discussions_by_contents',			#
							'get_discussions_by_created',			#
							'get_discussions_by_feed',				#
							'get_discussions_by_hot',				#
							'get_discussions_by_payout',			#
							'get_discussions_by_trending',			#
							'get_discussions_by_votes',				#
							'get_languages',						#
							'get_tags_used_by_author',				#
							'get_trending_tags'						#
							],
			"witness_api": [
							'get_active_witnesses',					# yes
							'get_miner_queue',						# bad
							'get_witness_by_account',				# yes "params": ["account"] возвращает параметры аккаунта если он делегат
							'get_witness_count',					# yes
							'get_witness_schedule',					# yes
							'get_witnesses',						# ??? "params": ["witnessIds"]
							'get_witnesses_by_vote',				# ??? "params": ["from", "limit"]
							'lookup_witness_accounts'				# yes
							],
		}
		
# Переделка списка апи под формат словаря name:api		
api_total = {}		
for key, value in api_list.items():
	for api in value:
		api_total[api] = key

		
# Список транзакций по порядку для каждого БЧ он свой
# https://github.com/VIZ-World/viz-world/blob/master/libraries/protocol/include/graphene/protocol/operations.hpp

# https://github.com/VIZ-World/viz-world-js/blob/master/src/auth/serializer/src/ChainTypes.js
# type https://github.com/VIZ-World/viz-world-js/blob/master/src/auth/serializer/src/operations.js
# type https://github.com/VIZ-World/viz-world-js/blob/master/src/auth/serializer/src/types.js
# params https://github.com/VIZ-World/viz-world-js/blob/master/src/broadcast/operations.js

# https://github.com/VIZ-Blockchain/viz-js-lib/blob/master/src/broadcast/operations.js
# https://github.com/VIZ-Blockchain/viz-js-lib/blob/master/src/auth/serializer/src/ChainTypes.js

#work with https://github.com/VIZ-Blockchain/viz-js-lib/blob/master/src/auth/serializer/src/operations.js

op_names = [
	'vote',									#0
	'content',								#1
	'transfer',								#2 yes
	'transfer_to_vesting',					#3 yes
	'withdraw_vesting',						#4 yes
	'account_update',						#5 yes
	'witness_update',						#6
	'account_witness_vote',					#7 yes
	'account_witness_proxy',				#8 yes
	'delete_content',						#9
	'custom',								#10 yes
	'set_withdraw_vesting_route',			#11 yes
	'request_account_recovery',				#12
	'recover_account',						#13
	'change_recovery_account',				#14 yes
	'escrow_transfer',						#15
	'escrow_dispute',						#16
	'escrow_release',						#17
	'escrow_approve',						#18
	'delegate_vesting_shares',				#19 yes
	'account_create',						#20 yes
	'account_metadata',						#21 yes
	'proposal_create',						#22
	'proposal_update',						#23
	'proposal_delete',						#24
	'chain_properties_update',				#25
	'author_reward',						#26
	'curation_reward',						#27
	'content_reward',						#28
	'fill_vesting_withdraw',				#29
	'shutdown_witness',						#30
	'hardfork',								#31
	'content_payout_update',				#32
	'content_benefactor_reward',			#33
	'return_vesting_delegation',			#34
	'committee_worker_create_request',		#35
	'committee_worker_cancel_request',		#36
	'committee_vote_request',				#37
	'committee_cancel_request',				#38
	'committee_approve_request',			#39
	'committee_payout_request',				#40
	'committee_pay_request',				#41
	'witness_reward',						#42
	'create_invite',						#43 yes
	'claim_invite_balance',					#44 yes
	'invite_registration',					#45 # рега аккаунта по одному ключу через инвайт
	'versioned_chain_properties_update',	#46
	'award',								#47 yes
	'receive_award',						#48
	'benefactor_award',						#49
	'set_paid_subscription',				#50
	'paid_subscribe',						#51
	'paid_subscription_action',				#52
	'cancel_paid_subscription',				#53
	'set_account_price',					#54
	'set_subaccount_price',					#55
	'buy_account',							#56
	'account_sale',							#57
]

#: assign operation ids
operations = dict(zip(op_names, range(len(op_names))))

asset_precision = {
					"VIZ": 3,
					"SHARES": 6,
					}



rus_d = {
		'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
		'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
		'й': 'ij', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
		'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
		'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'cz', 'ч': 'ch',
		'ш': 'sh', 'щ': 'shch', 'ъ': 'xx', 'ы': 'y', 'ь': 'x',
		'э': 'ye', 'ю': 'yu', 'я': 'ya',

		'А': "A", 'Б': "B", 'В': "V", 'Г': "G", 'Д': "D",
		'Е': "E", 'Ё': "yo", 'Ж': "ZH", 'З': "Z", 'И': "I",
		'Й': "IJ", 'К': "K", 'Л': "L", 'М': "M", 'Н': "N",
		'О': "O", 'П': "P", 'Р': "R", 'С': "S", 'Т': "T",
		'У': "U", 'Ф': "F", 'Х': "KH", 'Ц': "CZ", 'Ч': "CH",
		'Ш': "SH", 'Щ': "SHCH", 'Ъ': "XX", 'Ы': "Y", 'Ь': "X",
		'Э': "YE", 'Ю': "YU", 'Я': "YA",
		' ': "-",
		}

rus_list = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя., '