# -*- coding: utf-8 -*-

import requests

class Groups(object):
	def __init__(self, cfg):
		super(Groups, self).__init__()
		self.api = 'http://%s/api/v4/groups'
		self.source = cfg['source']
		self.target = cfg['target']

	def run(self):
		source = self.get()
		target = self.inserts(source)
		
		return { 'source': source, 'target': target }

	def get(self):
		resp = requests.get(
			self.api % self.source['address'], 
			headers = self.source['headers'])

		groups = sorted(resp.json(), key = lambda x:x['id'], reverse = False)

		print('Total groups: %d' % len(groups))

		return groups

	def inserts(self, groups):
		new_groups = []
		for group in groups:
			data = {
				"name": group['name'],
				"path": group['path'],
				"description": group['description'],
				"visibility": group['visibility'],
				"lfs_enabled": group['lfs_enabled']
			}
			resp = requests.post(
				self.api % self.target['address'], 
				headers = { 'PRIVATE-TOKEN': self.target['access_token'] }, 
				data = data)
			new_groups.append(resp.json())

		print('Create new group: %d' % len(new_groups))

		return new_groups
