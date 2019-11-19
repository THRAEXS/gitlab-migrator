# -*- coding: utf-8 -*-

import os, sys, requests, json, config

class Users(object):
	def __init__(self, env = 'test'):
		super(Users, self).__init__()
		self.api = 'http://%s/api/v4/users'
		self.source = config.SOURCE
		self.target = config.TARGET.get(env, config.TARGET['test'])

	def run(self):
		users = self.get()
		self.inserts(users)

	def get(self):
		resp = requests.get(
			self.api % self.source['address'], 
			headers = { 'PRIVATE-TOKEN': self.source['access_token'] }, 
			params = { 'per_page': 50 })

		users = sorted(resp.json(), key = lambda x:x['id'], reverse = False)
		with open('tmp/users.json', 'w', encoding = 'UTF-8') as f:
			json.dump(users, f, sort_keys = False, indent = 2, ensure_ascii = False)

		print('Total accounts: %d' % len(users))

		return users

	def inserts(self, users):
		c = 0
		for user in users:
			uname = user['username']
			if uname != 'root' and uname != 'ghost':
				data = {
					'email': user.get('email'),
					'password': '11111111',
					'username': user.get('username'),
					'name': user.get('name'),
					'skype': user.get('skype'),
					'linkedin ': user.get('linkedin '),
					'twitter': user.get('twitter'),
					'website_url': user.get('website_url'),
					'organization': user.get('organization'),
					'bio': user.get('bio'),
					'location': user.get('location'),
					'admin': user.get('is_admin'),
					'skip_confirmation': True
				}
				requests.post(
					self.api % self.target['address'], 
					headers = { 'PRIVATE-TOKEN': self.target['access_token'] }, 
					data = data)
				c += 1
		print('Create new user: %d' % c)

if __name__ == '__main__':
	env = sys.argv[1:]
	if env:
		env = env[0]
	else:
		env = 'test'

	tmppath = 'tmp'
	if not os.path.exists(tmppath):
		os.makedirs(tmppath)

	Users(env).run()
