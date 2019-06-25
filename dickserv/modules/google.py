#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# google.py

from googleapiclient.discovery import build

import config

def search(query, results):
	service = build('customsearch', 'v1', developerKey=config.api.google_api_key, cache_discovery=False)
	results = service.cse().list(q=query, cx=config.api.google_cse_id, num=results).execute()
	return results['items']