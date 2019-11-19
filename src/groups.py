# -*- coding: utf-8 -*-

import sys, requests, json, config

class Groups(object):
	def __init__(self, env = 'test'):
		super(Groups, self).__init__()
		self.api = 'http://%s/api/v4/groups'
		self.source = config.SOURCE
		self.target = config.TARGET.get(env, config.TARGET['test'])
		
	def run(self):
		groups = self.get()
		self.inserts(groups)

	def get(self):
		resp = requests.get(
			self.api % self.source['address'], 
			headers = { 'PRIVATE-TOKEN': self.source['access_token'] })

		groups = sorted(resp.json(), key = lambda x:x['id'], reverse = False)
		with open('tmp/groups.json', 'w', encoding = 'UTF-8') as f:
			json.dump(groups, f, sort_keys = False, indent = 2, ensure_ascii = False)

		print('Total groups: %d' % len(groups))

		return groups

	def inserts(self, groups):
		c = 0
		for group in groups:
			data = {
				"name": group['name'],
				"path": group['path'],
				"description": group['description'],
				"visibility": group['visibility'],
				"lfs_enabled": group['lfs_enabled']
			}
			requests.post(
				self.api % self.target['address'], 
				headers = { 'PRIVATE-TOKEN': self.target['access_token'] }, 
				data = data)
			c += 1
		print('Create new group: %d' % c)

if __name__ == '__main__':
	env = sys.argv[1:]
	if env:
		env = env[0]
	else:
		env = 'test'

	Groups(env).run()
