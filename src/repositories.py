# -*- coding: utf-8 -*-

from git import Repo
import os, shutil

project = 'admin-ui'
dirpath = 'tmp/repos/%s' % project

if os.path.exists(dirpath):
	# os.removedirs(dirpath)
	# os.rmdir(dirpath)
	# shutil.rmtree(dirpath)
	shutil.rmtree(dirpath, ignore_errors = True)

try:
	url = 'http://10.27.213.70/esp/admin-ui.git'
	repo = Repo.clone_from(url = url, to_path = dirpath, bare = True)
	# repo = Repo.clone_from(url = url, to_path = dirpath, branch = "dev")
except Exception as e:
	print('WARNING: repository[%s] already exists.' % project)
	repo = Repo(dirpath)

print('Repository:', repo)

try:
	gitlab = repo.create_remote('gitlab', 'http://10.122.163.77/esp/admin-ui.git')
except Exception as e:
	print('WARNING: remote gitlab already exists.')
	gitlab = repo.remotes.gitlab

print('Remotes:', repo.remotes)

# print((repo.remotes.origin))
# gl = repo.remotes.gitlab
# print(gl)
# print(gl.push)

# remote = repo.remotes[0]
# print(type(remote))
# print(remote)
# print(len(remote.refs))

git = repo.git
# git.checkout('origin/dev', b = 'dev')
print(git.branch)

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
