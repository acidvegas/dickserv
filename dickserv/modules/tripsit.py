#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# tripsit.py

import httplib

def drug(query):
	api = httplib.get_json('http://tripbot.tripsit.me/api/tripsit/getDrug?name=' + query.replace(' ','%20'))
	if api['err'] != True:
		return {'name':api['data'][0]['name'],'desc':api['data'][0]['properties']['summary']}
	else:
		return False