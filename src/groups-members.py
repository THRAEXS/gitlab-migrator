# -*- coding: utf-8 -*-

import os, sys, requests, json, config

class GroupsMembers(object):
	def __init__(self, env = 'test'):
		super(GroupsMembers, self).__init__()
		self.api = 'http://%s/api/v4/groups'
		self.source = config.SOURCE
		self.target = config.TARGET.get(env, config.TARGET['test'])
		
	def run(self):
		groups_members = self.get()
		self.inserts(groups_members)

	def get(self):
		# 获取目标gitlab下的groupes和users
		headers_target = { 'PRIVATE-TOKEN': self.target['access_token'] }
		target_groups = requests.get(self.api % self.target['address'],
			headers = headers_target).json()
		target_users = requests.get(
			'http://%s/api/v4/users?per_page=50' % self.target['address'],
			headers = headers_target).json()

		# 获取源gitlab的groups及其下的users
		headers_source = { 'PRIVATE-TOKEN': self.source['access_token'] }
		resp = requests.get(self.api % self.source['address'], 
			headers = headers_source)

		groups = sorted(resp.json(), key = lambda x:x['id'], reverse = False)
		groups_members = []
		for group in groups:
			tgroup = next(x for x in target_groups if x['name'] == group['name'])
			resp1 = requests.get(
				'%s/%s/members' % (self.api % self.source['address'], group['id']),
				headers = headers_source)
			members = resp1.json()
			for m in members:
				tm = next(x for x in target_users if x['username'] == m['username'])
				m['target_id'] = tm['id']
				m['target_username'] = tm['username']
			groups_members.append({
				'id': group['id'],
				'name': group['name'],
				'target_id': tgroup['id'],
				'target_name': tgroup['name'],
				'members': members
			})

		with open('tmp/groups-members.json', 'w', encoding = 'UTF-8') as f:
			json.dump(groups_members, f, sort_keys = False, indent = 2, ensure_ascii = False)

		return groups_members

	def inserts(self, groups_members):
		for gm in groups_members:
			gid = gm['target_id']
			print(gm['name'], len(gm['members']))
			for m in gm['members']:
				data = {
					'id': gid,
					'user_id': m['target_id'],
					'access_level': m['access_level']
				}
				requests.post(
					'%s/%s/members' % (self.api % self.target['address'], gid),
					headers = { 'PRIVATE-TOKEN': self.target['access_token'] }, 
					data = data)

if __name__ == '__main__':
	env = sys.argv[1:]
	if env:
		env = env[0]
	else:
		env = 'test'

	tmppath = 'tmp'
	if not os.path.exists(tmppath):
		os.makedirs(tmppath)

	GroupsMembers(env).run()
