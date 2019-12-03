# -*- coding: utf-8 -*-

import requests

class Projects(object):
	def __init__(self, cfg):
		super(Projects, self).__init__()
		self.api = 'http://%s/api/v4/projects'
		self.source = cfg['source']
		self.per_page = cfg['per_page']

	def run(self):
		projects = requests.get(
			self.api % self.source['address'], 
			headers = self.source['headers'],
			params = { 'order_by': 'updated_at', 'per_page': self.per_page }).json()
		
		print('Total projects:', len(projects))
		
		return projects
