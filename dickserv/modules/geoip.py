#!/usr/bin/env python
# DickServ IRC Service Bot
# Developed by acidvegas in Python 3
# https://github.com/acidvegas/dickserv/
# geoip.py

import httplib

def lookup(ip):
    api = httplib.get_json('http://freegeoip.net/json/' + ip)
    if api['city'] and api['region_name'] and api['country_name']:
        return '{0}, {1}, {2}'.format(api['city'], api['region_name'], api['country_name'])
    elif api['country_name']:
        return api['country_name']
    else:
        return False
