#!/usr/bin/env python
# DickServ IRC Service Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv
# vimeo.py

import re

import httplib

def check(url):
    return re.match(r'.*/(?P<id>\d+)', url)

def title(url):
    video_id = check(url).group('id')
    api      = 'https://vimeo.com/api/v2/video/%s.json' % video_id
    data     = httplib.get_json(api)
    return data['title']
