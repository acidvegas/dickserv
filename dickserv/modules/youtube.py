#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# youtube.py

import re

import config
import httplib

def check(url):
	found = re.match('^.*?youtu(be)?\.([a-z])+\/(watch(.*?)(\?|\&)v=)?(.*?)(&(.)*)*$', url, re.IGNORECASE)
	if found:
		return found.group(6)
	else:
		return False

def video_info(id):
	api = httplib.get_json(f'https://www.googleapis.com/youtube/v3/videos?key={config.api.google_api_key}&part=snippet,statistics&id={id}')
	if api['items']:
		api                 = api['items'][0]
		data                = {}
		data['channel']     = api['snippet']['channelTitle']
		data['description'] = ' '.join(api['snippet']['description'].split())
		data['dislikes']    = api['statistics']['dislikeCount']
		data['likes']       = api['statistics']['likeCount']
		data['title']       = api['snippet']['title']
		data['views']       = api['statistics']['viewCount']
		return data
	else:
		return False

def search(query, results):
	url	    = 'https://www.googleapis.com/youtube/v3/search?part=snippet&key={0}&q={1}&maxResults={2}&type=video&regionCode=US&relevanceLanguage=en&safeSearch=none'.format(config.api.google_api_key, httplib.data_quote(query), results)
	api     = httplib.get_json(url)
	results = {}
	for item in api['items']:
		title = item['snippet']['title']
		url   = 'https://www.youtube.com/watch?v=' + item['id']['videoId']
		results[title] = url
	return results
