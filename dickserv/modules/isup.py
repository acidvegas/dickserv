#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# isup.py

import httplib

def check(url):
    source = httplib.get_source('http://isup.me/' + url)
    if source.find('It\'s just you.') != -1:
        return 'UP'
    elif source.find('It\'s not just you!') != -1:
        return 'DOWN'
    elif source.find('Huh?') != -1:
        return 'INVALID'
    else:
        return 'UNKNOWN'
