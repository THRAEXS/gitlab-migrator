# -*- coding: utf-8 -*-

import json

def storage(name, data):
	with open('tmp/%s.json' % name, 'w', encoding = 'UTF-8') as f:
		json.dump(data, f, sort_keys = False, indent = 2, ensure_ascii = False)
