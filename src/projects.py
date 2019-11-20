# -*- coding: utf-8 -*-

import os, sys, requests, json, config

class Projects(object):
	def __init__(self, env = 'test'):
		super(Projects, self).__init__()
		self.api = 'http://%s/api/v4/projects'
		self.source = config.SOURCE
		self.target = config.TARGET.get(env, config.TARGET['test'])

	def run(self):
		self.get()

	def get(self):
		users = requests.get(
			'http://%s/api/v4/users' % self.source['address'], 
			headers = { 'PRIVATE-TOKEN': self.source['access_token'] }, 
			params = { 'per_page': 50 }).json()

		resp = requests.get(
			self.api % self.source['address'], 
			headers = { 'PRIVATE-TOKEN': self.source['access_token'] },
			params = { 'order_by': 'updated_at', 'per_page': 500 })

		projects = resp.json()
		print(len(projects))
		with open('tmp/projects.json', 'w', encoding = 'UTF-8') as f:
			json.dump(projects, f, sort_keys = False, indent = 2, ensure_ascii = False)

if __name__ == '__main__':
	env = sys.argv[1:]
	if env:
		env = env[0]
	else:
		env = 'test'

	tmppath = 'tmp'
	if not os.path.exists(tmppath):
		os.makedirs(tmppath)

	Projects(env).run()
