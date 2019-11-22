# -*- coding: utf-8 -*-

from git import Repo
# import os, shutil

dirpath = 'tmp/repos/admin-ui'
# if os.path.exists(dirpath):
# 	os.removedirs(dirpath)
	# shutil.rmtree(dirpath)
	# shutil.rmtree(dirpath, ignore_errors = True)

url = 'http://10.27.213.70/esp/admin-ui.git'
# repo = Repo.clone_from(url = url, to_path = dirpath)
# repo = Repo.clone_from(url = url, to_path = dirpath, branch = "dev")
repo = Repo(dirpath)

print(repo)
print(repo.remotes)
remote = repo.remotes[0]
print(type(remote))
print(remote)
print(len(remote.refs))
print(remote.refs)

git = repo.git
for ref in remote.refs:
	print(type(ref), ref)
	# git.checkout(ref, b = 'dev')
	if ref == 'origin/dev':
		print(1)
	# print(ref.__doc__)
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
