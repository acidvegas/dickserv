#!/usr/bin/env python
# DickServ IRC Service Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv
# vimeo.py

import re

import httplib

def check(url):
    return re.match(r'^(http://|https://)?(www\.)?(vimeo\.com/)?(\d+)', url)

def title(url):
    video_id = check(url).group(4)
    api      = 'https://vimeo.com/api/v2/video/{0}.json'.format(video_id)
    data     = httplib.get_json(api)
    return data[0]['title']
