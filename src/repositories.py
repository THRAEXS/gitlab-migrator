# -*- coding: utf-8 -*-

from git import Repo
import os, shutil

class Repositories(object):
	def __init__(self, cfg, source_projects):
		super(Repositories, self).__init__()
		self.api = 'http://%s/%s.git'
		self.source = cfg['source']
		self.target = cfg['target']
		self.source_projects = source_projects
		self.dirpath = 'tmp/repos/'

	def run(self):
		self.clean()
		for project in self.source_projects:
			groupdir = '%s%s' % (self.dirpath, project['namespace']['path'])
			if not os.path.exists(groupdir):
				os.makedirs(groupdir)
			self.push(project['path_with_namespace'], 
				'%s/%s' % (groupdir, project['path']))

	def push(self, uri, to_path):
		source_url = self.api % ('%s' % self.source['address'], uri)
		target_url = self.api % (self.target['address'], uri)
		print('Clone:', source_url)
		print('Push:', target_url)

		repo = Repo.clone_from(url = source_url, to_path = to_path, bare = True)
		gitlab = repo.create_remote('gitlab', target_url)
		gitlab.push(all = True)
		gitlab.push(tags = True)

	def clean(self):
		if os.path.exists(self.dirpath):
			shutil.rmtree(self.dirpath, onerror = self.onerror)

	def onerror(self, func, path, exec_info):
		import stat
		if not os.access(path, os.W_OK):
			os.chmod(path, stat.S_IWUSR)
			func(path)
		else:
			raise
