#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# shorturl.py

import httplib

def isgd(url):
    url = httplib.clean_url(url)
    api = httplib.get_source('http://is.gd/create.php?format=simple&url=' + url)
    if 'Error' in api:
        return False
    else:
        return api
    
def tinyurl(url):
    url = httplib.clean_url(url)
    return httplib.get_source('http://tinyurl.com/api-create.php?url=' + url)
