#!/usr/bin/env python
# DickServ IRC Service Bot
# Developed by acidvegas in Python 3

# https://github.com/acidvegas/dickserv/
# tripsit.py
# tripsit module developed by ioni

import httplib

def search(query):
    query = query.replace(' ', '%20')
    api   = httplib.get_json('http://tripbot.tripsit.me/api/tripsit/getDrug?name=' + query)
    return api
