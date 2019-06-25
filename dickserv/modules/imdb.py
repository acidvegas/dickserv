#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# imdb.py

import re

import config
import httplib

def check(url):
	found = re.match('^.*?imdb.com\/title\/tt([0-9A-Za-z]+).*?$', url, re.IGNORECASE)
	if found:
		return found.group(1)
	else:
		return False

def search(query):
	if query.startswith('tt') and len(query) == 9:
		api = httplib.get_json(f'http://omdbapi.com/?i={query}&apikey={config.api.omdbapi_key}')
	else:
		year = query.split()[-1]
		if len(year) == 4 and year.isdigit():
			query = query[:-5].replace(' ', '%20')
			api = httplib.get_json(f'http://omdbapi.com/?t={query}&y={year}&apikey={config.api.omdbapi_key}')
		else:
			query = query.replace(' ', '%20')
			api = httplib.get_json(f'http://omdbapi.com/?t={query}&apikey={config.api.omdbapi_key}')
	if api['Response'] == 'True':
		return api
	else:
		return False