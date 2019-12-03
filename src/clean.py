# -*- coding: utf-8 -*-

import requests, config

# 清除测试(test)目标的数据

cfg = config.TARGET['test']
address = 'http://%s/api/v4' % cfg['address']
headers = { 'PRIVATE-TOKEN': cfg['access_token'] }
print(address, headers)

def removeGroups():
	url = '%s/groups' % address
	resp = requests.get(url, headers = headers)
	groups = resp.json()
	print('Remove groups: %d' % len(groups))

	for g in groups:
		requests.delete('%s/%s' % (url, g['id']), headers = headers)

def removeUsers():
	url = '%s/users' % address
	resp = requests.get(url, headers = headers, 
		params = { 'per_page': 500 })
	users = resp.json()
	print('Remove users: %d' % len(users))

	for u in users:
		if u['username'] != 'root':
			requests.delete('%s/%s' % (url, u['id']), 
				headers = headers, params = { 'hard_delete': True })

def removeProjects():
	url = '%s/projects' % address
	projects = requests.get(url, headers = headers,
			params = { 'order_by': 'updated_at', 'per_page': 500 }).json()
	print('Remove projects: %d' % len(projects))
	
	for p in projects:
		requests.delete('%s/%s' % (url, p['id']), headers = headers)

class Clean(object):
	def __init__(self):
		super(Clean, self).__init__()
		removeGroups()
		removeUsers()
		removeProjects()

# def remove(ty):
# 	url = '%s/%s' % (address, ty)
# 	resp = requests.get(url, headers = headers)
# 	results = resp.json()
# 	print(url)
# 	print('Total %s: %d' % (ty, len(results)))	

# 	# user ?per_page=500
# 	for it in results:
# 		url1 = '%s/%s' % (url, it['id'])
# 		if ty == 'users':
# 			if it['username'] != 'root':
# 				requests.delete(url1, headers = headers, 
# 					params = { 'hard_delete': True })
# 		else:
# 			requests.delete(url1, headers = headers)

# remove('groups')
# remove('users')
