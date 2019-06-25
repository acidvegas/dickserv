#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# reddit.py

import re

import httplib
from database import Settings

def check(url):
	found = re.match('^.*?reddit.com\/r\/(.*?)\/comments\/([0-9A-Za-z]+).*$', url, re.IGNORECASE)
	if found:
		return (found.group(1), found.group(2))
	else:
		return False

def post_info(subreddit, id):
	api = httplib.get_json(f'https://www.reddit.com/r/{subreddit}/comments/{id}.json')
	if 'error' not in api:
		return api[0]['data']['children'][0]['data']
	else:
		return False

def read(subreddit):
	api  = httplib.get_json('https://www.reddit.com/r/{0}.json?limit={1}'.format(subreddit, Settings.get('max_results')))
	data = [x['data'] for x in api['data']['children']]
	if data:
		results = {}
		for item in data:
			if not item['stickied']:
				results[item['title']] = {'url':item['url'], 'score':item['score'], 'ups':item['ups'], 'downs':item['downs'], 'comments':item['num_comments']}
		return results
	else:
		return False
