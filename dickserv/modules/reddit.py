#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# reddit.py

import functions
import httplib

def read(subreddit):
    api     = httplib.get_json('http://www.reddit.com/r/' + subreddit + '.json?limit=10')
    data    = [x['data'] for x in api['data']['children']]
    results = {}
    if data:
        for item in data:
            if not item['stickied']:
                results[item['title']] = {'url':item['url'], 'score':item['score'], 'ups':item['ups'], 'downs':item['downs']}
        return results
    else:
        return False
