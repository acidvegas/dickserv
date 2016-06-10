#!/usr/bin/env python
# DickServ IRC Bot
# Developed by acidvegas in Python 3.5
# https://github.com/acidvegas/dickserv/
# imdb.py

import httplib

def search(query):
    query = query.replace(' ', '%20')
    api   = httplib.get_json('http://omdbapi.com/?t=' + query)
    if api['Response'] == 'True':
        return api
    else:
        return False
