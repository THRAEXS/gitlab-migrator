# -*- coding: utf-8 -*-

import requests

class Users(object):
	def __init__(self, cfg):
		super(Users, self).__init__()
		self.api = 'http://%s/api/v4/users'
		self.source = cfg['source']
		self.target = cfg['target']
		self.params = { 'per_page': cfg['per_page'], 'sort': 'asc' }

	def run(self):
		source = self.get()
		target = self.inserts(source)

		return { 'source': source, 'target': target }

	def get(self):
		resp = requests.get(self.api % self.source['address'], 
			headers = self.source['headers'], params = self.params)

		users = sorted(resp.json(), key = lambda x:x['id'], reverse = False)

		print('Total accounts: %d' % len(users))

		return users

	def inserts(self, users):
		new_users = []
		print('Old users size:', len(users))
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
				resp = requests.post(self.api % self.target['address'], 
					headers = self.target['headers'], data = data)
				new_users.append(resp.json())

		print('Create new user: %d' % len(new_users))

		resp = requests.get(self.api % self.target['address'], 
			headers = self.target['headers'], params = self.params)
		
		print('New user size: ', len(resp.json()))

		return resp.json()
