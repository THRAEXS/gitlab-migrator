# -*- coding: utf-8 -*-

import os, sys, requests, json, config

class GroupsMembers(object):
	def __init__(self, env = 'test'):
		super(GroupsMembers, self).__init__()
		self.api = 'http://%s/api/v4/groups'
		self.source = config.SOURCE
		self.target = config.TARGET.get(env, config.TARGET['test'])
		
	def run(self):
		members = self.get()
		# self.inserts(members)

	def get(self):
		resp = requests.get(
			self.api % self.source['address'], 
			headers = { 'PRIVATE-TOKEN': self.source['access_token'] })

		groups = sorted(resp.json(), key = lambda x:x['id'], reverse = False)
		groups_members = []
		for group in groups:
			resp1 = requests.get('%s/%s/members' % (
				self.api % self.source['address'],
				group['id']), headers = { 'PRIVATE-TOKEN': self.source['access_token'] })
			groups_members.append({
				'id': group['id'],
				'name': group['name'],
				'members': resp1.json()
			})

		with open('tmp/groups-members.json', 'w', encoding = 'UTF-8') as f:
			json.dump(groups_members, f, sort_keys = False, indent = 2, ensure_ascii = False)

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
