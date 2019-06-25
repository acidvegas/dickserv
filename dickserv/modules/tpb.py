#!/usr/bin/env python
# DickServ IRC Bot - Developed by acidvegas in Python (https://acid.vegas/dickserv)
# tpb.py

import re

import httplib
from database import Settings

def search(query, results):
	url      = 'https://thepiratebay.org/search/{0}/0/99/0'.format(query.replace(' ', '+'))
	source   = httplib.get_source(url)
	torrents = re.findall('<a href="(.*?)" class="detLink".*>(.*?)</a>', source)
	seeders  = re.findall('\t\t</td>\n\t\t<td align="right">(.*?)</td>', source)
	leechers = re.findall('<td align="right">(.*?)</td>\n\t</tr>',       source)
	if torrents:
		data     = {}
		torrents = torrents[:results]
		for i in range(len(torrents)):
			data[torrents[i][1]] = {'seeders':seeders[i], 'leechers':leechers[i], 'url':torrents[i][0]}
		return data
	else:
	   return False