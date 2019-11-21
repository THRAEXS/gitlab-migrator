# -*- coding: utf-8 -*-

import os, sys, requests, json, config
from io import BytesIO

class Projects(object):
	def __init__(self, env = 'test'):
		super(Projects, self).__init__()
		self.api = 'http://%s/api/v4/projects'
		self.source = config.SOURCE
		self.target = config.TARGET.get(env, config.TARGET['test'])

	def run(self):
		# self.get()
		self.mock()

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

	def mock(self):
		pid = 23
		headers = { 'PRIVATE-TOKEN': self.source['access_token'] }

		print('---------------------------------------------------')
		project = requests.get(
			'%s/%d' % (self.api % self.source['address'], pid), headers = headers).json()
		print('%s(%s/%s)' % (project['name'], project['path'], project['description']))

		print('\n---------------------------------------------------')
		links = project['_links']
		print(links['repo_branches'].replace(self.source['domain'], self.source['address']))
		branches = requests.get(links['repo_branches'] .replace(self.source['domain'], 
			self.source['address']), headers = headers).json()

		for b in branches:
			print('Branch name: %s' % b['name'])
		print('Total branches: %d' % len(branches))

		print('\n---------------------------------------------------')
		tag_list = requests.get(
			'%s/%d/repository/tags' % (self.api % self.source['address'], pid),
			headers = headers, params = { 'per_page':  500 }).json()
		print('Total tags: %d' % len(tag_list))

		# print('\n---------------------------------------------------')
		# data = {
		# 	'name': project['name'],
		# 	'path': project['path'],
		# 	'namespace_id': 100
		# }

		# c = requests.post(self.api % self.target['address'], 
		# 	headers = { 'PRIVATE-TOKEN': self.target['access_token'] }, 
		# 	data = data)
		# print(c)
		# print(c.json())

		print('\n---------------------------------------------------')
		# default: tar.gz
		resp = requests.get('%s/%d/repository/archive.tar.gz' % 
			(self.api % self.source['address'], pid), headers = headers)
		# with open('tmp/admin-ui.tar.gz', 'wb') as f:
		# 	f.write(resp.content)

		files = { 'file': ('tmp/admin-ui.tar.gz', BytesIO(resp.content)) }
		data = {
			'path': 'admin-ui',
			'namespace': 'esp'
		}
		target_headers = { 'PRIVATE-TOKEN': self.target['access_token'] }
		rr = requests.post('%s/import' % (self.api % self.target['address']),
			headers = target_headers, data = data, files = files)
		print(rr.json())

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
