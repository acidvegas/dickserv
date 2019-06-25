#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# netsplit.py

import re

import functions
import httplib

def search(query):
	channels = {}
	source   = httplib.get_source('http://irc.netsplit.de/channels/?chat=' + query.replace(' ','+'))
	for i in ('&#8203;','<b>','</b>','<span style="color:#000000;">','<strong>','</strong>'):
		source = source.replace(i, '')
	channel_objects = re.findall('<div style="margin: 4px; padding: 0 0 15 0; text-align: left;">(.*?)</a></span></div>', source, re.IGNORECASE|re.MULTILINE)
	for data in channel_objects:
		channel = functions.between(data, '<span class="cs-channel">', '</span>')
		network = functions.between(data, '<span class="cs-network">', '</span>')
		users   = functions.between(data, '<span class="cs-users">', ' &ndash; </span>')
		topic   = functions.between(data, '<span class="cs-topic">', '</span><br>')
		if not topic:
			topic = 'No channel topic set.'
		channels[channel] = {'network':network,'users':users,'topic':topic}
	return channels