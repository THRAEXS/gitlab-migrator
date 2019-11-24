# -*- coding: utf-8 -*-

from git import Repo
import os, shutil

class Repositories(object):
	def __init__(self, env = 'test'):
		super(Repositories, self).__init__()
		self.source = config.SOURCE
		self.target = config.TARGET.get(env, config.TARGET['test'])

	def run(self):
		projects = []
		for project in projects:
			namespace = project['path']
			tmppath = 'tmp/repos/%s' % namespace
			self.clean(tmppath)
			self.execute('%s.git' % namespace, tmppath)

	def execute(self, uri, to_path):
		repo = Repo.clone_from(
			url = 'http://%s/%s.git' % (self.source['address'], uri),
			to_path = to_path, bare = False)

		gitlab = repo.create_remote('gitlab', 
			'http://%s/%s.git' % (self.target['address'], uri))

		gitlab.push(all = True)
		gitlab.push(tags = True)

	def clean(self, dirpath):
		if os.path.exists(dirpath):
			shutil.rmtree(dirpath, onerror = onerror)

project = 'admin-ui'
dirpath = 'tmp/repos/%s' % project

def onerror(func, path, exec_info):
	import stat
	if not os.access(path, os.W_OK):
		os.chmod(path, stat.S_IWUSR)
		func(path)
	else:
		raise

if os.path.exists(dirpath):
	shutil.rmtree(dirpath, onerror = onerror)

# *******************
# url = 'http://10.27.213.70/esp/admin-ui.git'
# repo = Repo.clone_from(url = url, to_path = dirpath, bare = False)
# # repo = Repo.clone_from(url = url, to_path = dirpath, branch = "dev")
# print('Repository:', repo)

# gitlab = repo.create_remote('gitlab', 'http://10.122.163.77/esp/admin-ui.git')
# print('Remotes:', repo.remotes)

# # Create new branch
# git = repo.git
# # print(git.branch.__doc__)
# print(type(git.branch()))
# # print(git.branch())
# print(repo.remotes.origin.refs)
# # <git.RemoteReference "refs/remotes/origin/dev">
# # test = repo.create_head('test1', commit = repo.remotes.origin.refs[1])
# test = repo.create_head('test1', commit = 'origin/dev')
# print(test)
# print(type(test))
# *******************

# gitlab.push(all = True)
# gitlab.push(tags = True)

# print((repo.remotes.origin))
# gl = repo.remotes.gitlab
# print(gl)
# print(gl.push)

# remote = repo.remotes[0]
# print(type(remote))
# print(remote)
# print(len(remote.refs))

# git = repo.git
# git.checkout('origin/dev', b = 'dev')
# print(git.branch)

# 循环推送分支
# for ref in remote.refs:
# 	print(type(ref), ref, ref.name, type(ref.name))
# 	if ref.name != 'origin/HEAD':
# 		print('push', ref.name)
# 		bname = ref.name.replace('origin/', '')
# 		# git push gitlab dev:dev
# 		# gl.push(refspec = '{}:{}'.format(bname, bname))

# 		# git push gitlab dev
# 		gl.push(refspec = bname)

# gl.push(all = True)
# gl.push(tags = True)

# info = remote.push()[0]
# print(type(info.flags), info.flags)
# print(type(info.local_ref), info.local_ref)
# print(type(info.remote_ref_string), info.remote_ref_string)
# print(type(info.remote_ref), info.remote_ref)
# print(type(info.old_commit), info.old_commit)
# print(type(info.summary), info.summary)

# git = repo.git
# print(git)
# git.checkout('origin/dev', b = 'dev')
# print(repo.is_dirty())
# print(repo.git.status())
